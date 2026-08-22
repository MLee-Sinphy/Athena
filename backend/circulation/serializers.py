from rest_framework import serializers

from .models import (
    CalendarException,
    InternalNotice,
    Loan,
    PolicyVersion,
    RegularOpening,
    Reservation,
)


class PolicyVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyVersion
        fields = (
            "id",
            "effective_from",
            "min_loan_days",
            "max_loan_days",
            "simultaneous_loan_limit",
            "pickup_tolerance_days",
            "late_penalty_days",
            "cancellation_limit",
            "cancellation_window_days",
            "globally_suspended",
        )
        read_only_fields = ("id", "effective_from")


class RegularOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularOpening
        fields = ("weekday", "is_open")


class CalendarExceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarException
        fields = ("id", "date", "is_open", "label")
        read_only_fields = ("id",)


class ReservationSerializer(serializers.ModelSerializer):
    queue_position = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ("id", "title", "copy", "start_date", "end_date", "state", "queue_position")
        read_only_fields = ("id", "copy", "state", "queue_position")

    def get_queue_position(self, obj):
        queue_request = getattr(obj, "queue_request", None)
        return queue_request.position if queue_request and queue_request.active else None


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ("id", "reservation", "checked_out_at", "due_date", "returned_on")
        read_only_fields = fields


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalNotice
        fields = ("id", "kind", "payload", "created_at", "read_at", "response")
        read_only_fields = ("id", "kind", "payload", "created_at", "read_at")
