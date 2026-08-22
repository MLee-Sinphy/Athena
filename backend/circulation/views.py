from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import AdministratorOnly, PasswordChanged

from .models import InternalNotice, Loan, NoticeResponse, PolicyVersion, RegularOpening, Reservation
from .serializers import (
    CalendarExceptionSerializer,
    LoanSerializer,
    NoticeSerializer,
    PolicyVersionSerializer,
    RegularOpeningSerializer,
    ReservationSerializer,
)
from .services import (
    AllocationConflict,
    accept_early_opportunity,
    cancel_reservation,
    change_reservation,
    checkout_reservation,
    create_reservation,
    renew_loan,
    return_loan,
)


class PolicyView(APIView):
    permission_classes = [AdministratorOnly]

    def get(self, request):
        policy = PolicyVersion.objects.first()
        return Response(PolicyVersionSerializer(policy).data if policy else None)

    def post(self, request):
        previous = PolicyVersion.objects.first()
        before = PolicyVersionSerializer(previous).data if previous else {}
        serializer = PolicyVersionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        policy = serializer.save()
        from governance.services import record_audit

        record_audit(
            request.user,
            "policy_version_created",
            policy,
            dict(before),
            dict(serializer.data),
            request.data.get("reason", ""),
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegularOpeningView(APIView):
    permission_classes = [AdministratorOnly]

    def put(self, request, weekday):
        opening, _ = RegularOpening.objects.get_or_create(weekday=weekday)
        before = {"weekday": opening.weekday, "is_open": opening.is_open}
        serializer = RegularOpeningSerializer(opening, data={**request.data, "weekday": weekday})
        serializer.is_valid(raise_exception=True)
        opening = serializer.save()
        from governance.services import record_audit

        record_audit(
            request.user,
            "regular_opening_changed",
            opening,
            before,
            dict(serializer.data),
            request.data.get("reason", ""),
        )
        return Response(serializer.data)


class CalendarExceptionView(APIView):
    permission_classes = [AdministratorOnly]

    def post(self, request):
        serializer = CalendarExceptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        exception = serializer.save()
        from governance.services import record_audit

        record_audit(
            request.user,
            "calendar_exception_created",
            exception,
            {},
            dict(serializer.data),
            request.data.get("reason", ""),
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReservationView(APIView):
    permission_classes = [PasswordChanged]

    def get(self, request):
        reservations = Reservation.objects.filter(reader=request.user).select_related(
            "queue_request"
        )
        return Response({"results": ReservationSerializer(reservations, many=True).data})

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            reservation = create_reservation(
                request.user.id, data["title"].id, data["start_date"], data["end_date"]
            )
        except AllocationConflict:
            return Response({"detail": "Reservation is not eligible."}, status=409)
        return Response(ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED)


class ReservationDetailView(APIView):
    permission_classes = [PasswordChanged]

    def patch(self, request, reservation_id):
        serializer = ReservationSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        reservation = Reservation.objects.get(pk=reservation_id, reader=request.user)
        try:
            changed = change_reservation(
                reservation.id,
                request.user.id,
                serializer.validated_data.get("start_date", reservation.start_date),
                serializer.validated_data.get("end_date", reservation.end_date),
            )
        except AllocationConflict:
            return Response({"detail": "Requested dates conflict."}, status=409)
        return Response(ReservationSerializer(changed).data)

    def delete(self, request, reservation_id):
        cancel_reservation(reservation_id, request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckoutView(APIView):
    permission_classes = [PasswordChanged]

    def post(self, request, reservation_id):
        try:
            loan = checkout_reservation(reservation_id, request.user.id, timezone.now())
        except AllocationConflict:
            return Response({"detail": "Checkout is not allowed."}, status=409)
        return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)


class ReturnView(APIView):
    permission_classes = [PasswordChanged]

    def post(self, request, loan_id):
        loan = Loan.objects.get(pk=loan_id, reservation__reader=request.user)
        returned = return_loan(loan.id, timezone.localdate())
        return Response(LoanSerializer(returned).data)


class LoanListView(APIView):
    permission_classes = [PasswordChanged]

    def get(self, request):
        loans = Loan.objects.filter(reservation__reader=request.user)
        return Response({"results": LoanSerializer(loans, many=True).data})


class RenewView(APIView):
    permission_classes = [PasswordChanged]

    def post(self, request, loan_id):
        try:
            loan = renew_loan(loan_id, request.user.id, request.data.get("due_date"))
        except (AllocationConflict, TypeError):
            return Response({"detail": "Renewal is not allowed."}, status=409)
        return Response(LoanSerializer(loan).data)


class NoticeView(APIView):
    permission_classes = [PasswordChanged]

    def get(self, request, notice_id=None):
        notices = InternalNotice.objects.filter(recipient=request.user)
        return Response({"results": NoticeSerializer(notices, many=True).data})

    def post(self, request, notice_id=None):
        response = request.data.get("response")
        if response not in NoticeResponse.values:
            return Response({"response": ["Invalid response."]}, status=400)
        notice = accept_early_opportunity(notice_id, request.user.id, response)
        return Response(NoticeSerializer(notice).data)


class AdminReservationInterventionView(APIView):
    permission_classes = [AdministratorOnly]

    def patch(self, request, reservation_id):
        reservation = Reservation.objects.get(pk=reservation_id)
        before = {
            "state": reservation.state,
            "start_date": reservation.start_date.isoformat(),
            "end_date": reservation.end_date.isoformat(),
        }
        try:
            changed = change_reservation(
                reservation.id,
                reservation.reader_id,
                request.data.get("start_date", reservation.start_date),
                request.data.get("end_date", reservation.end_date),
            )
        except (AllocationConflict, TypeError):
            return Response({"detail": "Intervention conflicts with another period."}, status=409)
        from governance.services import record_audit

        record_audit(
            request.user,
            "reservation_changed",
            changed,
            before,
            {
                "state": changed.state,
                "start_date": changed.start_date.isoformat(),
                "end_date": changed.end_date.isoformat(),
            },
            request.data.get("reason", ""),
        )
        return Response(ReservationSerializer(changed).data)

    def delete(self, request, reservation_id):
        reservation = Reservation.objects.get(pk=reservation_id)
        before = {"state": reservation.state}
        cancelled = cancel_reservation(reservation_id, request.user.id, administrative=True)
        from governance.services import record_audit

        record_audit(
            request.user,
            "reservation_cancelled",
            cancelled,
            before,
            {"state": cancelled.state},
            request.data.get("reason", ""),
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
