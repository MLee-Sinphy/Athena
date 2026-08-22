from django.core.exceptions import ValidationError

from circulation.models import Loan

from .models import AuditEntry, Rating, TagSuggestion


def submit_return_feedback(loan_id, reader_id, title_score=None, copy_score=None, tags=None):
    loan = Loan.objects.select_related("reservation").get(pk=loan_id)
    if loan.reservation.reader_id != reader_id or not loan.returned_on:
        raise ValidationError("Feedback is only available to the reader after return.")
    if (
        Rating.objects.filter(loan=loan).exists()
        or TagSuggestion.objects.filter(loan=loan).exists()
    ):
        raise ValidationError("Feedback has already been submitted.")
    rating = None
    if title_score is not None or copy_score is not None:
        rating = Rating(loan=loan, title_score=title_score, copy_score=copy_score)
        rating.full_clean()
        rating.save()
    for name in tags or []:
        normalized = name.strip().lower().removeprefix("#")
        if normalized:
            TagSuggestion.objects.create(
                loan=loan, title=loan.reservation.title, author_id=reader_id, name=normalized
            )
    return rating


def record_audit(actor, action, target, before, after, reason=""):
    return AuditEntry.objects.create(
        actor=actor,
        action=action,
        target_type=target.__class__.__name__,
        target_id=str(target.pk),
        before=before,
        after=after,
        reason=reason or "",
    )
