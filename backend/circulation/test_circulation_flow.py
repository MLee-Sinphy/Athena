from datetime import date, timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from accounts.authentication import issue_token
from catalog.models import BookCopy, BookTitle, CopyState
from circulation.models import (
    InternalNotice,
    Loan,
    NoticeResponse,
    PolicyVersion,
    ReservationState,
)
from circulation.services import (
    AllocationConflict,
    accept_early_opportunity,
    cancel_reservation,
    change_reservation,
    checkout_reservation,
    create_reservation,
    mark_missed_pickups,
    renew_loan,
    return_loan,
)

from .test_policy_domain import make_title, make_user


class ReservationFlowTests(TestCase):
    def setUp(self):
        self.policy = PolicyVersion.objects.create()
        self.reader = make_user("FLOW-A")
        self.other = make_user("FLOW-B")
        self.title = make_title()
        self.copy = BookCopy.objects.create(
            title=self.title,
            internal_code="FLOW-001",
            state=CopyState.AVAILABLE,
            condition_rating=5,
        )
        self.start = date(2026, 9, 7)
        self.end = date(2026, 9, 11)

    def test_valid_request_is_automatic_and_conflict_enters_fifo_waiting_list(self):
        first = create_reservation(self.reader.id, self.title.id, self.start, self.end)
        second = create_reservation(self.other.id, self.title.id, self.start, self.end)

        self.assertEqual(first.state, ReservationState.CONFIRMED)
        self.assertEqual(second.state, ReservationState.WAITING)
        self.assertEqual(second.queue_request.position, 1)

    def test_checkout_is_idempotent_and_only_then_creates_active_loan(self):
        reservation = create_reservation(self.reader.id, self.title.id, self.start, self.end)

        first = checkout_reservation(reservation.id, self.reader.id, at=timezone.now())
        second = checkout_reservation(reservation.id, self.reader.id, at=timezone.now())

        self.assertEqual(first.id, second.id)
        self.assertEqual(Loan.objects.count(), 1)
        self.copy.refresh_from_db()
        self.assertEqual(self.copy.state, CopyState.LOANED)

    def test_return_is_idempotent_frees_copy_and_late_return_creates_penalty(self):
        reservation = create_reservation(self.reader.id, self.title.id, self.start, self.end)
        loan = checkout_reservation(reservation.id, self.reader.id, at=timezone.now())
        returned_on = self.end + timedelta(days=1)

        first = return_loan(loan.id, returned_on)
        second = return_loan(loan.id, returned_on)

        self.assertEqual(first.returned_on, second.returned_on)
        self.assertTrue(self.reader.penalty_set.filter(reason="late_return").exists())
        self.copy.refresh_from_db()
        self.assertEqual(self.copy.state, CopyState.AVAILABLE)

    def test_dates_change_before_pickup_but_conflicting_change_is_atomic(self):
        reservation = create_reservation(self.reader.id, self.title.id, self.start, self.end)
        changed = change_reservation(
            reservation.id, self.reader.id, date(2026, 9, 14), date(2026, 9, 18)
        )
        create_reservation(self.other.id, self.title.id, self.start, self.end)

        with self.assertRaises(AllocationConflict):
            change_reservation(changed.id, self.reader.id, self.start, self.end)
        changed.refresh_from_db()
        self.assertEqual(changed.start_date, date(2026, 9, 14))

    def test_renewal_changes_only_due_date_within_maximum_and_without_queue(self):
        reservation = create_reservation(self.reader.id, self.title.id, self.start, self.end)
        loan = checkout_reservation(reservation.id, self.reader.id, at=timezone.now())

        renewed = renew_loan(loan.id, self.reader.id, date(2026, 9, 18))
        self.assertEqual(renewed.due_date, date(2026, 9, 18))

        create_reservation(self.other.id, self.title.id, date(2026, 9, 21), date(2026, 9, 25))
        with self.assertRaises(AllocationConflict):
            renew_loan(loan.id, self.reader.id, date(2026, 9, 21))

    def test_reader_cancellation_is_counted_and_preserves_history(self):
        reservation = create_reservation(self.reader.id, self.title.id, self.start, self.end)

        cancel_reservation(reservation.id, self.reader.id)

        reservation.refresh_from_db()
        self.assertEqual(reservation.state, ReservationState.CANCELLED)
        self.assertEqual(self.reader.cancellationevent_set.count(), 1)

    def test_fourth_cancellation_blocks_new_requests_until_window_end(self):
        for index in range(4):
            reservation = create_reservation(
                self.reader.id,
                self.title.id,
                self.start + timedelta(days=index * 7),
                self.end + timedelta(days=index * 7),
            )
            cancel_reservation(reservation.id, self.reader.id)

        with self.assertRaises(AllocationConflict):
            create_reservation(self.reader.id, self.title.id, date(2026, 11, 2), date(2026, 11, 6))

    def test_administrator_can_cancel_without_counting_against_reader(self):
        reservation = create_reservation(self.reader.id, self.title.id, self.start, self.end)
        admin = make_user("TEMP-ADMIN")
        admin.role = "administrator"
        admin.save(update_fields=["role"])
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {issue_token(admin)}")

        response = client.delete(f"/api/v1/admin/reservations/{reservation.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertTrue(self.reader.cancellationevent_set.get().administrative)


class MissedPickupAndNoticeTests(TestCase):
    def setUp(self):
        self.policy = PolicyVersion.objects.create(pickup_tolerance_days=1)
        self.first = make_user("MISS-A")
        self.next = make_user("MISS-B")
        self.title = BookTitle.objects.create(
            name="Fila",
            author="Autora",
            publisher="Editora",
            edition="1",
            publication_year=2024,
            category="Teste",
            description="Descrição.",
            cover="covers/queue.jpg",
        )
        BookCopy.objects.create(title=self.title, internal_code="QUEUE-001", condition_rating=4)
        self.original = create_reservation(
            self.first.id, self.title.id, date(2026, 8, 24), date(2026, 9, 4)
        )
        self.waiting = create_reservation(
            self.next.id, self.title.id, date(2026, 8, 31), date(2026, 9, 4)
        )

    def test_next_reader_accepts_early_pickup_and_original_reader_is_notified_privately(self):
        mark_missed_pickups(date(2026, 8, 26))
        notice = InternalNotice.objects.get(recipient=self.next, kind="early_opportunity")

        accept_early_opportunity(notice.id, self.next.id, NoticeResponse.ACCEPTED)

        self.waiting.refresh_from_db()
        self.original.refresh_from_db()
        self.assertEqual(self.waiting.state, ReservationState.CONFIRMED)
        self.assertEqual(self.waiting.end_date, date(2026, 9, 4))
        self.assertEqual(self.original.state, ReservationState.NEEDS_RESCHEDULE)
        displaced = InternalNotice.objects.get(recipient=self.first, kind="interval_displaced")
        self.assertNotIn(self.next.email, str(displaced.payload))

    def test_refusal_is_recorded_and_does_not_remove_original_dates(self):
        mark_missed_pickups(date(2026, 8, 26))
        notice = InternalNotice.objects.get(recipient=self.next, kind="early_opportunity")

        accept_early_opportunity(notice.id, self.next.id, NoticeResponse.DECLINED)

        notice.refresh_from_db()
        self.original.refresh_from_db()
        self.assertEqual(notice.response, NoticeResponse.DECLINED)
        self.assertEqual(self.original.state, ReservationState.CONFIRMED)

    def test_api_exposes_only_current_readers_queue_and_notices(self):
        mark_missed_pickups(date(2026, 8, 26))
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {issue_token(self.next)}")

        reservations = client.get("/api/v1/reservations/")
        notices = client.get("/api/v1/notices/")

        combined = str(reservations.data) + str(notices.data)
        self.assertEqual(reservations.status_code, 200)
        self.assertEqual(notices.status_code, 200)
        self.assertNotIn(self.first.email, combined)
        self.assertNotIn(self.first.registration_id, combined)
