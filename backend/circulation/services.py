from datetime import timedelta

from django.db import connection, transaction
from django.utils import timezone

from catalog.models import BookCopy, CopyState

from .models import (
    CalendarException,
    CancellationEvent,
    Penalty,
    PolicyVersion,
    RegularOpening,
    Reservation,
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


@transaction.atomic
def allocate_copy(reader_id, title_id, start_date, end_date, policy_id):
    policy = PolicyVersion.objects.get(pk=policy_id)
    if policy.globally_suspended or not validate_loan_period(start_date, end_date, policy):
        raise AllocationConflict
    today = timezone.localdate()
    penalties = Penalty.objects.filter(
        reader_id=reader_id, starts_on__lte=today, ends_on__gte=today
    )
    if penalties.exists():
        raise AllocationConflict
    active_count = Reservation.objects.filter(
        reader_id=reader_id, state=ReservationState.CONFIRMED, end_date__gte=today
    ).count()
    reduction = sum(penalty.loan_limit_reduction for penalty in penalties)
    if active_count >= max(0, policy.simultaneous_loan_limit - reduction):
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
