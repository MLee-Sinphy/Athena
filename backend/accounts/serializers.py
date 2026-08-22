from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(trim_whitespace=False, write_only=True)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "registration_id", "role", "must_change_password")
        read_only_fields = ("id", "registration_id", "role", "must_change_password")

    def validate_email(self, value):
        query = get_user_model().objects.filter(email__iexact=value)
        if self.instance:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise serializers.ValidationError("This email address is already in use.")
        return value


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(trim_whitespace=False, write_only=True)
    new_password = serializers.CharField(trim_whitespace=False, write_only=True)

    def validate_new_password(self, value):
        validate_password(value, self.context["request"].user)
        return value


class PasswordResetSerializer(serializers.Serializer):
    temporary_password = serializers.CharField(trim_whitespace=False, write_only=True)

    def validate_temporary_password(self, value):
        validate_password(value)
        return value


class ReaderCreateSerializer(serializers.ModelSerializer):
    temporary_password = serializers.CharField(trim_whitespace=False, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "registration_id", "temporary_password")
        read_only_fields = ("id",)

    def validate_email(self, value):
        if get_user_model().objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email address is already in use.")
        return value

    def validate_temporary_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("temporary_password")
        return get_user_model().objects.create_user(password=password, **validated_data)
