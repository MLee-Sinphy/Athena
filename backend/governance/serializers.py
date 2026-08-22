from rest_framework import serializers

from .models import AuditEntry, Rating


class FeedbackSerializer(serializers.Serializer):
    title_score = serializers.IntegerField(min_value=1, max_value=5, required=False)
    copy_score = serializers.IntegerField(min_value=1, max_value=5, required=False)
    tags = serializers.ListField(
        child=serializers.CharField(max_length=80), required=False, allow_empty=True
    )


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("id", "loan", "title_score", "copy_score", "created_at")
        read_only_fields = fields


class AuditEntrySerializer(serializers.ModelSerializer):
    actor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = AuditEntry
        fields = (
            "id",
            "actor",
            "action",
            "target_type",
            "target_id",
            "before",
            "after",
            "reason",
            "created_at",
        )
        read_only_fields = fields
