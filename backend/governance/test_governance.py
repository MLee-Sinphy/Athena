from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from accounts.authentication import issue_token
from catalog.models import BookCopy, CopyState
from circulation.models import PolicyVersion
from circulation.services import checkout_reservation, create_reservation, return_loan
from circulation.test_policy_domain import make_title, make_user
from governance.models import AuditEntry, Rating, TagSuggestion, VisualConfiguration
from governance.services import submit_return_feedback


class FeedbackTests(TestCase):
    def setUp(self):
        PolicyVersion.objects.create()
        self.reader = make_user("RATING")
        self.other = make_user("RATING-OTHER")
        self.title = make_title()
        BookCopy.objects.create(
            title=self.title,
            internal_code="RATING-001",
            state=CopyState.AVAILABLE,
            condition_rating=4,
        )
        reservation = create_reservation(
            self.reader.id, self.title.id, date(2026, 9, 7), date(2026, 9, 11)
        )
        self.loan = checkout_reservation(reservation.id, self.reader.id, timezone.now())

    def test_only_responsible_reader_rates_returned_loan_once_with_optional_scores(self):
        with self.assertRaises(ValidationError):
            submit_return_feedback(self.loan.id, self.reader.id, title_score=5)
        return_loan(self.loan.id, date(2026, 9, 11))
        rating = submit_return_feedback(
            self.loan.id, self.reader.id, title_score=5, copy_score=None
        )

        self.assertEqual(rating.title_score, 5)
        with self.assertRaises(ValidationError):
            submit_return_feedback(self.loan.id, self.reader.id, title_score=4)
        with self.assertRaises(ValidationError):
            submit_return_feedback(self.loan.id, self.other.id, title_score=4)

    def test_suggested_tags_preserve_author_and_date_and_participate_in_search(self):
        return_loan(self.loan.id, date(2026, 9, 11))
        submit_return_feedback(self.loan.id, self.reader.id, tags=["filosofia medieval"])
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {issue_token(self.reader)}")

        response = client.get("/api/v1/catalog/titles/?q=%23filosofia%20medieval")

        suggestion = TagSuggestion.objects.get()
        self.assertEqual(suggestion.author, self.reader)
        self.assertIsNotNone(suggestion.created_at)
        self.assertEqual(len(response.data["results"]), 1)

    def test_averages_are_derived_from_individual_ratings(self):
        return_loan(self.loan.id, date(2026, 9, 11))
        submit_return_feedback(self.loan.id, self.reader.id, title_score=5, copy_score=3)

        self.assertEqual(Rating.objects.title_average(self.title), 5)
        self.assertEqual(Rating.objects.copy_average(self.loan.reservation.copy), 3)


class AuditAndAnalyticsTests(TestCase):
    def setUp(self):
        PolicyVersion.objects.create()
        self.reader = make_user("AUDIT-READER")
        self.admin = make_user("AUDIT-ADMIN")
        self.admin.role = "administrator"
        self.admin.save(update_fields=["role"])
        self.title = make_title()
        BookCopy.objects.create(
            title=self.title,
            internal_code="AUDIT-001",
            state=CopyState.AVAILABLE,
            condition_rating=4,
        )
        self.reservation = create_reservation(
            self.reader.id, self.title.id, date(2026, 10, 5), date(2026, 10, 9)
        )
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {issue_token(self.admin)}")

    def test_admin_intervention_records_immutable_before_after_and_optional_reason(self):
        response = self.client.delete(
            f"/api/v1/admin/reservations/{self.reservation.id}/",
            {"reason": "Solicitação"},
            format="json",
        )

        self.assertEqual(response.status_code, 204)
        entry = AuditEntry.objects.get()
        self.assertEqual(entry.actor, self.admin)
        self.assertEqual(entry.before["state"], "confirmed")
        self.assertEqual(entry.after["state"], "cancelled")
        self.assertEqual(entry.reason, "Solicitação")
        entry.reason = "alterado"
        with self.assertRaises(ValidationError):
            entry.save()
        with self.assertRaises(ValidationError):
            entry.delete()
        with self.assertRaises(ValidationError):
            AuditEntry.objects.filter(pk=entry.pk).update(reason="alterado")

    def test_analytics_are_rebuilt_from_history_without_personal_identifiers(self):
        loan = checkout_reservation(self.reservation.id, self.reader.id, timezone.now())
        return_loan(loan.id, date(2026, 10, 9))

        response = self.client.get("/api/v1/admin/analytics/circulation/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["by_title"][0]["loan_count"], 1)
        self.assertEqual(response.data["by_category"][0]["loan_count"], 1)
        self.assertEqual(response.data["by_period"][0]["returned_on"], date(2026, 10, 9))
        self.assertNotIn(self.reader.email, str(response.data))
        self.assertNotIn(self.reader.registration_id, str(response.data))


class VisualConfigurationTests(TestCase):
    def setUp(self):
        self.admin = make_user("THEME-ADMIN")
        self.admin.role = "administrator"
        self.admin.save(update_fields=["role"])
        self.reader = make_user("THEME-READER")

    def test_administrator_selects_global_theme_and_change_is_audited(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {issue_token(self.admin)}")

        response = client.patch(
            "/api/v1/admin/configuration/visual/", {"theme": "aqua"}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(VisualConfiguration.load().theme, "aqua")
        self.assertEqual(AuditEntry.objects.get().action, "visual_configuration_changed")
        self.assertEqual(APIClient().get("/api/v1/health/").data["theme"], "aqua")

    def test_reader_cannot_change_global_theme_and_unknown_theme_is_rejected(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {issue_token(self.reader)}")
        self.assertEqual(
            client.patch(
                "/api/v1/admin/configuration/visual/", {"theme": "wine"}, format="json"
            ).status_code,
            403,
        )
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {issue_token(self.admin)}")
        self.assertEqual(
            client.patch(
                "/api/v1/admin/configuration/visual/", {"theme": "unknown"}, format="json"
            ).status_code,
            400,
        )
