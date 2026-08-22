from django.urls import path

from .views import CalendarExceptionView, PolicyView, RegularOpeningView

urlpatterns = [
    path("admin/policies/", PolicyView.as_view(), name="policy"),
    path("admin/calendar/regular/<int:weekday>/", RegularOpeningView.as_view(), name="opening"),
    path("admin/calendar/exceptions/", CalendarExceptionView.as_view(), name="calendar-exception"),
]
