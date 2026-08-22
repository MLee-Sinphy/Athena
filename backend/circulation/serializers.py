from rest_framework import serializers

from .models import CalendarException, PolicyVersion, RegularOpening


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
