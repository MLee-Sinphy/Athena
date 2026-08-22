from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F, Q

from catalog.models import BookCopy, BookTitle


class RegularOpening(models.Model):
    weekday = models.PositiveSmallIntegerField(
        unique=True, validators=[MinValueValidator(0), MaxValueValidator(6)]
    )
    is_open = models.BooleanField(default=True)

    class Meta:
        ordering = ["weekday"]

    def __str__(self):
        return f"Weekday {self.weekday}: {'open' if self.is_open else 'closed'}"


class CalendarException(models.Model):
    date = models.DateField(unique=True)
    is_open = models.BooleanField(default=False)
    label = models.CharField(max_length=160)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.date}: {self.label}"


class PolicyVersion(models.Model):
    effective_from = models.DateTimeField(auto_now_add=True)
    min_loan_days = models.PositiveSmallIntegerField(default=3)
    max_loan_days = models.PositiveSmallIntegerField(default=15)
    simultaneous_loan_limit = models.PositiveSmallIntegerField(default=3)
    pickup_tolerance_days = models.PositiveSmallIntegerField(default=1)
    late_penalty_days = models.PositiveSmallIntegerField(default=7)
    cancellation_limit = models.PositiveSmallIntegerField(default=3)
    cancellation_window_days = models.PositiveSmallIntegerField(default=30)
    globally_suspended = models.BooleanField(default=False)

    class Meta:
        ordering = ["-effective_from", "-id"]
        constraints = [
            models.CheckConstraint(
                condition=Q(max_loan_days__gte=F("min_loan_days")),
                name="policy_max_days_gte_min_days",
            )
        ]

    def __str__(self):
        return f"Policy {self.pk} from {self.effective_from}"


class ReservationState(models.TextChoices):
    WAITING = "waiting", "Waiting"
    CONFIRMED = "confirmed", "Confirmed"
    CANCELLED = "cancelled", "Cancelled"
    COMPLETED = "completed", "Completed"
    NEEDS_RESCHEDULE = "needs_reschedule", "Needs reschedule"


class Reservation(models.Model):
    reader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.ForeignKey(BookTitle, on_delete=models.PROTECT, related_name="reservations")
    copy = models.ForeignKey(
        BookCopy, on_delete=models.PROTECT, related_name="reservations", null=True, blank=True
    )
    start_date = models.DateField()
    end_date = models.DateField()
    state = models.CharField(max_length=20, choices=ReservationState)
    policy = models.ForeignKey(PolicyVersion, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    exclusivity_lost_at = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["created_at", "id"]
        constraints = [
            models.CheckConstraint(
                condition=Q(end_date__gte=F("start_date")),
                name="reservation_end_gte_start",
            ),
            models.CheckConstraint(
                condition=Q(state=ReservationState.WAITING, copy__isnull=True)
                | ~Q(state=ReservationState.WAITING),
                name="waiting_reservation_has_no_copy",
            ),
        ]

    def __str__(self):
        return f"Reservation {self.pk} ({self.state})"


class ReservationRequestQuerySet(models.QuerySet):
    def for_title(self, title):
        return self.filter(title=title, active=True).order_by("created_at", "id")


class ReservationRequest(models.Model):
    reader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.ForeignKey(BookTitle, on_delete=models.PROTECT, related_name="requests")
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    reservation = models.OneToOneField(
        Reservation, on_delete=models.CASCADE, related_name="queue_request", null=True, blank=True
    )

    objects = ReservationRequestQuerySet.as_manager()

    class Meta:
        ordering = ["created_at", "id"]

    def __str__(self):
        return f"Request {self.pk}"

    @property
    def position(self):
        return (
            ReservationRequest.objects.for_title(self.title)
            .filter(
                Q(created_at__lt=self.created_at) | Q(created_at=self.created_at, id__lte=self.id)
            )
            .count()
        )


class CancellationEvent(models.Model):
    reader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    occurred_at = models.DateTimeField()
    administrative = models.BooleanField(default=False)

    class Meta:
        ordering = ["occurred_at", "id"]

    def __str__(self):
        return f"Cancellation {self.pk}"


class Penalty(models.Model):
    reader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    reason = models.CharField(max_length=160)
    starts_on = models.DateField()
    ends_on = models.DateField()
    loan_limit_reduction = models.PositiveSmallIntegerField(default=0)
    blocks_new = models.BooleanField(default=True)

    class Meta:
        ordering = ["starts_on", "id"]
        constraints = [
            models.CheckConstraint(
                condition=Q(ends_on__gte=F("starts_on")), name="penalty_end_gte_start"
            )
        ]

    def __str__(self):
        return f"Penalty {self.pk}: {self.reason}"


class Loan(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.PROTECT, related_name="loan")
    checked_out_at = models.DateTimeField()
    due_date = models.DateField()
    returned_on = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-checked_out_at", "-id"]

    def __str__(self):
        return f"Loan {self.pk}"


class NoticeResponse(models.TextChoices):
    ACCEPTED = "accepted", "Accepted"
    DECLINED = "declined", "Declined"


class InternalNotice(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="notices"
    )
    kind = models.CharField(max_length=80)
    payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    response = models.CharField(max_length=20, choices=NoticeResponse, blank=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"Notice {self.pk}: {self.kind}"
