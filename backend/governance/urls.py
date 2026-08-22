from django.urls import path

from .views import (
    AuditListView,
    CirculationAnalyticsView,
    FeedbackView,
    VisualConfigurationView,
)

urlpatterns = [
    path("loans/<int:loan_id>/feedback/", FeedbackView.as_view(), name="loan-feedback"),
    path("admin/audit/", AuditListView.as_view(), name="audit-list"),
    path("admin/analytics/circulation/", CirculationAnalyticsView.as_view(), name="analytics"),
    path("admin/configuration/visual/", VisualConfigurationView.as_view(), name="visual-config"),
]
