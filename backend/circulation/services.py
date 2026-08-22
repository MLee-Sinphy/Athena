from datetime import timedelta

from django.db import connection, transaction
from django.utils import timezone

from catalog.models import BookCopy, CopyState

from .models import (
    CalendarException,
    CancellationEvent,
    InternalNotice,
    Loan,
    NoticeResponse,
    Penalty,
    PolicyVersion,
    RegularOpening,
    Reservation,
    ReservationRequest,
    ReservationState,
)


class AllocationConflict(Exception):
    pass


def is_open_day(day):
    exception = CalendarException.objects.filter(date=day).first()
    if exception:
        return exception.is_open
    configured = RegularOpening.objects.filter(weekday=day.weekday()).first()
    return configured.is_open if configured else day.weekday() < 5


def count_open_days(start_date, end_date):
    if end_date < start_date:
        return 0
    count = 0
    current = start_date
    while current <= end_date:
        count += int(is_open_day(current))
        current += timedelta(days=1)
    return count


def validate_loan_period(start_date, end_date, policy):
    duration = count_open_days(start_date, end_date)
    return policy.min_loan_days <= duration <= policy.max_loan_days


def late_blocked_until(returned_at, policy):
    return returned_at + timedelta(days=policy.late_penalty_days)


def cancellation_blocked_until(reader, at, policy):
    window_start = at - timedelta(days=policy.cancellation_window_days)
    events = CancellationEvent.objects.filter(
        reader=reader,
        administrative=False,
        occurred_at__gte=window_start,
        occurred_at__lte=at,
    ).order_by("occurred_at", "id")
    if events.count() <= policy.cancellation_limit:
        return None
    return events.first().occurred_at.date() + timedelta(days=policy.cancellation_window_days)


def _lock_copy(copy_id):
    if connection.vendor == "postgresql":
        with connection.cursor() as cursor:
            cursor.execute("SELECT pg_advisory_xact_lock(%s)", [copy_id])
    else:
        BookCopy.objects.select_for_update().get(pk=copy_id)


def _reader_is_eligible(reader_id, policy):
    today = timezone.localdate()
    penalties = Penalty.objects.filter(
        reader_id=reader_id, starts_on__lte=today, ends_on__gte=today
    )
    if penalties.filter(blocks_new=True).exists():
        return False
    active_count = Reservation.objects.filter(
        reader_id=reader_id, state=ReservationState.CONFIRMED, end_date__gte=today
    ).count()
    reduction = sum(penalty.loan_limit_reduction for penalty in penalties)
    return active_count < max(0, policy.simultaneous_loan_limit - reduction)


@transaction.atomic
def allocate_copy(reader_id, title_id, start_date, end_date, policy_id):
    policy = PolicyVersion.objects.get(pk=policy_id)
    if policy.globally_suspended or not validate_loan_period(start_date, end_date, policy):
        raise AllocationConflict
    if not _reader_is_eligible(reader_id, policy):
        raise AllocationConflict

    copies = BookCopy.objects.filter(title_id=title_id, state=CopyState.AVAILABLE).order_by("id")
    for copy in copies:
        _lock_copy(copy.id)
        overlap = Reservation.objects.filter(
            copy_id=copy.id,
            state=ReservationState.CONFIRMED,
            start_date__lte=end_date,
            end_date__gte=start_date,
        ).exists()
        if not overlap:
            return Reservation.objects.create(
                reader_id=reader_id,
                title_id=title_id,
                copy_id=copy.id,
                start_date=start_date,
                end_date=end_date,
                state=ReservationState.CONFIRMED,
                policy=policy,
            )
    raise AllocationConflict


def current_policy():
    policy = PolicyVersion.objects.first()
    return policy or PolicyVersion.objects.create()


def create_reservation(reader_id, title_id, start_date, end_date):
    policy = current_policy()
    if (
        policy.globally_suspended
        or not validate_loan_period(start_date, end_date, policy)
        or not _reader_is_eligible(reader_id, policy)
    ):
        raise AllocationConflict
    try:
        return allocate_copy(reader_id, title_id, start_date, end_date, policy.id)
    except AllocationConflict:
        with transaction.atomic():
            reservation = Reservation.objects.create(
                reader_id=reader_id,
                title_id=title_id,
                start_date=start_date,
                end_date=end_date,
                state=ReservationState.WAITING,
                policy=policy,
            )
            ReservationRequest.objects.create(
                reader_id=reader_id, title_id=title_id, reservation=reservation
            )
            return reservation


@transaction.atomic
def checkout_reservation(reservation_id, reader_id, at):
    reservation = Reservation.objects.select_for_update().get(
        pk=reservation_id, reader_id=reader_id
    )
    existing = Loan.objects.filter(reservation=reservation).first()
    if existing:
        return existing
    if reservation.state != ReservationState.CONFIRMED or not reservation.copy_id:
        raise AllocationConflict
    loan = Loan.objects.create(
        reservation=reservation, checked_out_at=at, due_date=reservation.end_date
    )
    reservation.copy.state = CopyState.LOANED
    reservation.copy.save(update_fields=["state", "updated_at"])
    return loan


@transaction.atomic
def return_loan(loan_id, returned_on):
    loan = (
        Loan.objects.select_for_update()
        .select_related("reservation__copy", "reservation__reader", "reservation__policy")
        .get(pk=loan_id)
    )
    if loan.returned_on:
        return loan
    loan.returned_on = returned_on
    loan.save(update_fields=["returned_on"])
    loan.reservation.state = ReservationState.COMPLETED
    loan.reservation.save(update_fields=["state"])
    loan.reservation.copy.state = CopyState.AVAILABLE
    loan.reservation.copy.save(update_fields=["state", "updated_at"])
    if returned_on > loan.due_date:
        Penalty.objects.create(
            reader=loan.reservation.reader,
            reason="late_return",
            starts_on=returned_on,
            ends_on=late_blocked_until(returned_on, loan.reservation.policy),
        )
    return loan


@transaction.atomic
def change_reservation(reservation_id, reader_id, start_date, end_date):
    reservation = Reservation.objects.select_for_update().get(
        pk=reservation_id, reader_id=reader_id
    )
    if hasattr(reservation, "loan") or reservation.state != ReservationState.CONFIRMED:
        raise AllocationConflict
    if not validate_loan_period(start_date, end_date, reservation.policy):
        raise AllocationConflict
    conflict = (
        Reservation.objects.filter(
            copy_id=reservation.copy_id,
            state=ReservationState.CONFIRMED,
            start_date__lte=end_date,
            end_date__gte=start_date,
        )
        .exclude(pk=reservation.pk)
        .exists()
    )
    if conflict:
        raise AllocationConflict
    reservation.start_date = start_date
    reservation.end_date = end_date
    reservation.save(update_fields=["start_date", "end_date"])
    return reservation


@transaction.atomic
def cancel_reservation(reservation_id, reader_id, administrative=False):
    reservation = Reservation.objects.select_for_update().get(pk=reservation_id)
    if not administrative and reservation.reader_id != reader_id:
        raise AllocationConflict
    if reservation.state != ReservationState.CANCELLED:
        reservation.state = ReservationState.CANCELLED
        reservation.save(update_fields=["state"])
        event = CancellationEvent.objects.create(
            reader=reservation.reader, occurred_at=timezone.now(), administrative=administrative
        )
        blocked_until = cancellation_blocked_until(
            reservation.reader, event.occurred_at, reservation.policy
        )
        if blocked_until:
            Penalty.objects.get_or_create(
                reader=reservation.reader,
                reason="cancellation_limit",
                starts_on=event.occurred_at.date(),
                ends_on=blocked_until,
            )
        ReservationRequest.objects.filter(reservation=reservation).update(active=False)
    return reservation


@transaction.atomic
def renew_loan(loan_id, reader_id, new_due_date):
    loan = (
        Loan.objects.select_for_update()
        .select_related("reservation__policy")
        .get(pk=loan_id, reservation__reader_id=reader_id, returned_on__isnull=True)
    )
    reservation = loan.reservation
    if not validate_loan_period(reservation.start_date, new_due_date, reservation.policy):
        raise AllocationConflict
    queue_or_future = (
        Reservation.objects.filter(
            title_id=reservation.title_id,
            state__in=[ReservationState.WAITING, ReservationState.CONFIRMED],
            end_date__gte=loan.due_date,
        )
        .exclude(pk=reservation.pk)
        .exists()
    )
    if queue_or_future:
        raise AllocationConflict
    loan.due_date = new_due_date
    loan.save(update_fields=["due_date"])
    reservation.end_date = new_due_date
    reservation.save(update_fields=["end_date"])
    return loan


def mark_missed_pickups(on_date):
    reservations = Reservation.objects.filter(
        state=ReservationState.CONFIRMED,
        start_date__lt=on_date,
        loan__isnull=True,
        exclusivity_lost_at__isnull=True,
    ).select_related("policy")
    for reservation in reservations:
        elapsed = count_open_days(reservation.start_date, on_date) - 1
        if elapsed <= reservation.policy.pickup_tolerance_days:
            continue
        reservation.exclusivity_lost_at = on_date
        reservation.save(update_fields=["exclusivity_lost_at"])
        next_request = (
            ReservationRequest.objects.for_title(reservation.title)
            .select_related("reservation")
            .first()
        )
        if next_request:
            InternalNotice.objects.get_or_create(
                recipient=next_request.reader,
                kind="early_opportunity",
                payload={
                    "reservation_id": next_request.reservation_id,
                    "original_reservation_id": reservation.id,
                    "available_on": on_date.isoformat(),
                },
            )


@transaction.atomic
def accept_early_opportunity(notice_id, reader_id, response):
    notice = InternalNotice.objects.select_for_update().get(pk=notice_id, recipient_id=reader_id)
    if notice.response:
        return notice
    notice.read_at = timezone.now()
    notice.response = response
    notice.save(update_fields=["read_at", "response"])
    if response == NoticeResponse.DECLINED:
        return notice
    waiting = Reservation.objects.select_for_update().get(pk=notice.payload["reservation_id"])
    original = Reservation.objects.select_for_update().get(
        pk=notice.payload["original_reservation_id"]
    )
    waiting.copy = original.copy
    waiting.start_date = notice.payload["available_on"]
    waiting.state = ReservationState.CONFIRMED
    waiting.save(update_fields=["copy", "start_date", "state"])
    ReservationRequest.objects.filter(reservation=waiting).update(active=False)
    original.state = ReservationState.NEEDS_RESCHEDULE
    original.copy = None
    original.save(update_fields=["state", "copy"])
    InternalNotice.objects.create(
        recipient=original.reader,
        kind="interval_displaced",
        payload={"reservation_id": original.id},
    )
    return notice
