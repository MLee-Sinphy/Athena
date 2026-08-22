from datetime import UTC, date, datetime, timedelta
from threading import Barrier, Thread

from django.contrib.auth import get_user_model
from django.db import close_old_connections, connection
from django.test import TestCase, TransactionTestCase
from django.utils import timezone
from rest_framework.test import APIClient

from accounts.authentication import issue_token
from catalog.models import BookCopy, BookTitle
from circulation.models import (
    CalendarException,
    CancellationEvent,
    Penalty,
    PolicyVersion,
    RegularOpening,
    Reservation,
    ReservationRequest,
    ReservationState,
)
from circulation.services import (
    AllocationConflict,
    allocate_copy,
    cancellation_blocked_until,
    count_open_days,
    late_blocked_until,
    validate_loan_period,
)


def make_user(suffix):
    return get_user_model().objects.create_user(
        email=f"reader-{suffix}@example.com",
        registration_id=f"CAL-{suffix}",
        password="a valid library passphrase",
        must_change_password=False,
    )


def make_title():
    return BookTitle.objects.create(
        name="Calendário",
        author="Autora",
        publisher="Editora",
        edition="1",
        publication_year=2024,
        category="Teste",
        description="Descrição.",
        cover="covers/calendar.jpg",
    )


class CalendarAndPolicyTests(TestCase):
    def test_default_calendar_counts_monday_to_friday_and_configured_closure(self):
        CalendarException.objects.create(date=date(2026, 8, 25), is_open=False, label="Fechado")

        self.assertEqual(count_open_days(date(2026, 8, 24), date(2026, 8, 30)), 4)

    def test_exception_can_open_a_weekend(self):
        CalendarException.objects.create(date=date(2026, 8, 29), is_open=True, label="Plantão")

        self.assertEqual(count_open_days(date(2026, 8, 29), date(2026, 8, 29)), 1)

    def test_period_respects_configurable_minimum_and_maximum_open_days(self):
        policy = PolicyVersion.objects.create(min_loan_days=3, max_loan_days=15)

        self.assertFalse(validate_loan_period(date(2026, 8, 24), date(2026, 8, 25), policy))
        self.assertTrue(validate_loan_period(date(2026, 8, 24), date(2026, 8, 26), policy))
        self.assertFalse(validate_loan_period(date(2026, 8, 24), date(2026, 9, 14), policy))

    def test_policy_change_does_not_retroactively_change_confirmed_reservation(self):
        user = make_user("POLICY")
        title = make_title()
        copy = BookCopy.objects.create(title=title, internal_code="POL-1", condition_rating=4)
        original = PolicyVersion.objects.create(max_loan_days=15)
        reservation = Reservation.objects.create(
            reader=user,
            title=title,
            copy=copy,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 10),
            state=ReservationState.CONFIRMED,
            policy=original,
        )
        PolicyVersion.objects.create(max_loan_days=7)

        reservation.refresh_from_db()
        self.assertEqual(reservation.policy.max_loan_days, 15)


class PenaltyBoundaryTests(TestCase):
    def test_late_return_blocks_for_default_seven_calendar_days(self):
        policy = PolicyVersion.objects.create(late_penalty_days=7)
        returned_at = date(2026, 8, 22)

        self.assertEqual(late_blocked_until(returned_at, policy), date(2026, 8, 29))

    def test_more_than_three_reader_cancellations_in_rolling_window_blocks_until_window_end(self):
        reader = make_user("CANCEL")
        policy = PolicyVersion.objects.create(cancellation_limit=3, cancellation_window_days=30)
        first = datetime(2026, 8, 1, 12, tzinfo=UTC)
        for offset in (0, 2, 4, 6):
            CancellationEvent.objects.create(
                reader=reader, occurred_at=first + timedelta(days=offset)
            )

        self.assertEqual(
            cancellation_blocked_until(reader, first + timedelta(days=6), policy),
            first.date() + timedelta(days=30),
        )

    def test_administrative_cancellation_does_not_count(self):
        reader = make_user("ADMIN-CANCEL")
        policy = PolicyVersion.objects.create(cancellation_limit=3, cancellation_window_days=30)
        now = timezone.now()
        for offset in range(4):
            CancellationEvent.objects.create(
                reader=reader, occurred_at=now - timedelta(days=offset), administrative=True
            )

        self.assertIsNone(cancellation_blocked_until(reader, now, policy))

    def test_active_penalty_blocks_new_allocation_without_cancelling_existing_one(self):
        reader = make_user("PENALTY")
        title = make_title()
        BookCopy.objects.create(title=title, internal_code="PEN-1", condition_rating=4)
        policy = PolicyVersion.objects.create()
        today = timezone.localdate()
        Penalty.objects.create(
            reader=reader, reason="Late return", starts_on=today, ends_on=today + timedelta(days=7)
        )

        with self.assertRaises(AllocationConflict):
            allocate_copy(reader.id, title.id, date(2026, 9, 1), date(2026, 9, 5), policy.id)

    def test_global_suspension_blocks_only_new_allocations(self):
        reader = make_user("SUSPENDED")
        title = make_title()
        copy = BookCopy.objects.create(title=title, internal_code="SUS-1", condition_rating=4)
        old_policy = PolicyVersion.objects.create()
        existing = Reservation.objects.create(
            reader=reader,
            title=title,
            copy=copy,
            start_date=date(2026, 10, 1),
            end_date=date(2026, 10, 5),
            state=ReservationState.CONFIRMED,
            policy=old_policy,
        )
        suspended = PolicyVersion.objects.create(globally_suspended=True)

        with self.assertRaises(AllocationConflict):
            allocate_copy(reader.id, title.id, date(2026, 11, 2), date(2026, 11, 6), suspended.id)
        self.assertTrue(Reservation.objects.filter(pk=existing.pk).exists())


class FifoTests(TestCase):
    def test_requests_use_creation_time_then_monotonic_id_without_exposing_other_reader(self):
        title = make_title()
        first = ReservationRequest.objects.create(reader=make_user("FIFO-A"), title=title)
        second = ReservationRequest.objects.create(reader=make_user("FIFO-B"), title=title)
        same_time = timezone.now()
        ReservationRequest.objects.filter(pk__in=[first.pk, second.pk]).update(created_at=same_time)

        ordered = list(ReservationRequest.objects.for_title(title).values_list("id", flat=True))

        self.assertEqual(ordered, [first.id, second.id])


class PolicyAdministrationTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            email="policy-admin@example.com",
            registration_id="POLICY-ADMIN",
            password="an administrative passphrase",
        )
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {issue_token(self.admin)}")

    def test_administrator_versions_policy_and_customizes_open_days(self):
        policy = self.client.post(
            "/api/v1/admin/policies/", {"min_loan_days": 4, "max_loan_days": 12}, format="json"
        )
        sunday = self.client.put(
            "/api/v1/admin/calendar/regular/6/", {"is_open": True}, format="json"
        )
        closure = self.client.post(
            "/api/v1/admin/calendar/exceptions/",
            {"date": "2026-09-07", "is_open": False, "label": "Feriado"},
            format="json",
        )

        self.assertEqual(policy.status_code, 201)
        self.assertEqual(sunday.status_code, 200)
        self.assertEqual(closure.status_code, 201)
        self.assertTrue(RegularOpening.objects.get(weekday=6).is_open)

    def test_reader_cannot_change_policy(self):
        reader = make_user("NO-POLICY")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {issue_token(reader)}")

        response = self.client.post("/api/v1/admin/policies/", {}, format="json")

        self.assertEqual(response.status_code, 403)


class AllocationConcurrencyTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.title = make_title()
        BookCopy.objects.create(title=self.title, internal_code="CONCURRENT-1", condition_rating=5)
        self.policy = PolicyVersion.objects.create()
        self.users = [make_user("RACE-A"), make_user("RACE-B")]

    def test_two_concurrent_requests_never_confirm_same_copy_period(self):
        if connection.vendor != "postgresql":
            self.skipTest("Concurrency gate runs against PostgreSQL in CI.")
        barrier = Barrier(2)
        outcomes = []

        def attempt(user_id):
            close_old_connections()
            barrier.wait()
            try:
                reservation = allocate_copy(
                    user_id, self.title.id, date(2026, 9, 1), date(2026, 9, 5), self.policy.id
                )
                outcomes.append(("confirmed", reservation.id))
            except AllocationConflict:
                outcomes.append(("conflict", None))
            finally:
                close_old_connections()

        threads = [Thread(target=attempt, args=(user.id,)) for user in self.users]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(sorted(result[0] for result in outcomes), ["confirmed", "conflict"])
        self.assertEqual(Reservation.objects.filter(state=ReservationState.CONFIRMED).count(), 1)
