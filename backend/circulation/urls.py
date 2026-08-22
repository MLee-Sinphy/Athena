from django.urls import path

from .views import (
    AdminReservationInterventionView,
    CalendarExceptionView,
    CheckoutView,
    LoanListView,
    NoticeView,
    PolicyView,
    RegularOpeningView,
    RenewView,
    ReservationDetailView,
    ReservationView,
    ReturnView,
)

urlpatterns = [
    path("admin/policies/", PolicyView.as_view(), name="policy"),
    path("admin/calendar/regular/<int:weekday>/", RegularOpeningView.as_view(), name="opening"),
    path("admin/calendar/exceptions/", CalendarExceptionView.as_view(), name="calendar-exception"),
    path("reservations/", ReservationView.as_view(), name="reservation-list"),
    path(
        "reservations/<int:reservation_id>/",
        ReservationDetailView.as_view(),
        name="reservation-detail",
    ),
    path("reservations/<int:reservation_id>/checkout/", CheckoutView.as_view(), name="checkout"),
    path("loans/<int:loan_id>/return/", ReturnView.as_view(), name="return"),
    path("loans/", LoanListView.as_view(), name="loan-list"),
    path("loans/<int:loan_id>/renew/", RenewView.as_view(), name="renew"),
    path("notices/", NoticeView.as_view(), name="notice-list"),
    path("notices/<int:notice_id>/respond/", NoticeView.as_view(), name="notice-response"),
    path(
        "admin/reservations/<int:reservation_id>/",
        AdminReservationInterventionView.as_view(),
        name="admin-reservation-intervention",
    ),
]
