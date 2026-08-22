from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg

from catalog.models import BookTitle
from circulation.models import Loan


class VisualTheme(models.TextChoices):
    CALCULUS = "calculus", "Calculus"
    OCEAN = "ocean", "Ocean"
    WINE = "wine", "Wine"
    SLATE = "slate", "Slate"
    INDIGO = "indigo", "Indigo"
    AQUA = "aqua", "Aqua Glass"


class VisualConfiguration(models.Model):
    theme = models.CharField(max_length=20, choices=VisualTheme, default=VisualTheme.CALCULUS)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_theme_display()

    def save(self, *args, **kwargs):
        self.pk = 1
        return super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        configuration, _ = cls.objects.get_or_create(pk=1)
        return configuration


class RatingQuerySet(models.QuerySet):
    def title_average(self, title):
        return self.filter(loan__reservation__title=title).aggregate(value=Avg("title_score"))[
            "value"
        ]

    def copy_average(self, copy):
        return self.filter(loan__reservation__copy=copy).aggregate(value=Avg("copy_score"))["value"]


class Rating(models.Model):
    loan = models.OneToOneField(Loan, on_delete=models.PROTECT, related_name="rating")
    title_score = models.PositiveSmallIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    copy_score = models.PositiveSmallIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = RatingQuerySet.as_manager()

    def __str__(self):
        return f"Rating for loan {self.loan_id}"


class TagSuggestion(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.PROTECT, related_name="tag_suggestions")
    title = models.ForeignKey(BookTitle, on_delete=models.PROTECT, related_name="tag_suggestions")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    name = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]
        constraints = [models.UniqueConstraint(fields=["loan", "name"], name="unique_tag_per_loan")]

    def __str__(self):
        return f"#{self.name}"


class ImmutableAuditQuerySet(models.QuerySet):
    def update(self, **kwargs):
        raise ValidationError("Audit entries are immutable.")

    def delete(self):
        raise ValidationError("Audit entries cannot be deleted.")


class AuditEntry(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    action = models.CharField(max_length=120)
    target_type = models.CharField(max_length=120)
    target_id = models.CharField(max_length=120)
    before = models.JSONField(default=dict)
    after = models.JSONField(default=dict)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ImmutableAuditQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.action} {self.target_type}:{self.target_id}"

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError("Audit entries are immutable.")
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Audit entries cannot be deleted.")
