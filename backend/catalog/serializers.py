from pathlib import Path

from rest_framework import serializers

from .models import BookCopy, BookImage, BookTitle, CopyState, Tag

IMAGE_SIGNATURES = (b"\xff\xd8\xff", b"\x89PNG\r\n\x1a\n", b"RIFF")
IMAGE_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}


def validate_image_upload(value):
    if value.size > 5 * 1024 * 1024:
        raise serializers.ValidationError("Image must not exceed 5 MB.")
    content_type = getattr(value, "content_type", "")
    header = value.read(12)
    value.seek(0)
    extension = Path(value.name).suffix.lower()
    signature_valid = any(header.startswith(signature) for signature in IMAGE_SIGNATURES)
    if content_type not in IMAGE_CONTENT_TYPES or extension not in {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    }:
        raise serializers.ValidationError("Only JPEG, PNG, and WebP images are accepted.")
    if not signature_valid:
        raise serializers.ValidationError("The uploaded file is not a valid supported image.")
    return value


class ReaderCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = ("id", "condition_rating")


class CatalogTitleSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    available_copies = serializers.IntegerField(read_only=True)
    cover = serializers.SerializerMethodField()

    class Meta:
        model = BookTitle
        fields = (
            "id",
            "name",
            "author",
            "publisher",
            "edition",
            "publication_year",
            "category",
            "description",
            "cover",
            "isbn",
            "page_count",
            "metadata_source_url",
            "tags",
            "available_copies",
        )

    def get_cover(self, obj):
        if not obj.cover.name:
            return ""
        request = self.context.get("request")
        path = f"/api/v1/catalog/media/{obj.cover.name}"
        return request.build_absolute_uri(path) if request else path


class CatalogTitleDetailSerializer(CatalogTitleSerializer):
    copies = serializers.SerializerMethodField()

    class Meta(CatalogTitleSerializer.Meta):
        fields = CatalogTitleSerializer.Meta.fields + ("copies",)

    def get_copies(self, obj):
        copies = obj.copies.filter(state=CopyState.AVAILABLE)
        return ReaderCopySerializer(copies, many=True).data


class AdminTitleSerializer(serializers.ModelSerializer):
    cover = serializers.FileField(validators=[validate_image_upload])
    tag_names = serializers.ListField(
        child=serializers.CharField(max_length=80), write_only=True, required=False
    )

    class Meta:
        model = BookTitle
        fields = (
            "id",
            "name",
            "author",
            "publisher",
            "edition",
            "publication_year",
            "category",
            "description",
            "cover",
            "isbn",
            "page_count",
            "metadata_source_url",
            "tag_names",
        )
        read_only_fields = ("metadata_source_url",)

    def create(self, validated_data):
        tag_names = validated_data.pop("tag_names", [])
        title = super().create(validated_data)
        title.tags.set(
            Tag.objects.get_or_create(name=name.strip().lower())[0] for name in tag_names
        )
        return title

    def update(self, instance, validated_data):
        tag_names = validated_data.pop("tag_names", None)
        title = super().update(instance, validated_data)
        if tag_names is not None:
            title.tags.set(
                Tag.objects.get_or_create(name=name.strip().lower())[0] for name in tag_names
            )
        return title


class AdminCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = ("id", "title", "internal_code", "state", "condition_rating")


class AdminBookImageSerializer(serializers.ModelSerializer):
    image = serializers.FileField(validators=[validate_image_upload])

    class Meta:
        model = BookImage
        fields = ("id", "title", "image", "alt_text")
