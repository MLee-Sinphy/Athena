from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=80, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"#{self.name}"


class BookTitle(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    edition = models.CharField(max_length=100)
    publication_year = models.PositiveSmallIntegerField()
    category = models.CharField(max_length=120)
    description = models.TextField()
    cover = models.FileField(upload_to="covers/")
    isbn = models.CharField(max_length=20, blank=True)
    page_count = models.PositiveIntegerField(null=True, blank=True)
    metadata_source_url = models.URLField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="titles")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name", "author", "id"]
        indexes = [models.Index(fields=["name"]), models.Index(fields=["author"])]

    def __str__(self):
        return self.name


class BookImage(models.Model):
    title = models.ForeignKey(BookTitle, on_delete=models.CASCADE, related_name="additional_images")
    image = models.FileField(upload_to="books/")
    alt_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.alt_text


class CopyState(models.TextChoices):
    AVAILABLE = "available", "Available"
    RESERVED = "reserved", "Reserved"
    LOANED = "loaned", "Loaned"
    LOST = "lost", "Lost"
    DISCARDED = "discarded", "Discarded"


class BookCopy(models.Model):
    title = models.ForeignKey(BookTitle, on_delete=models.PROTECT, related_name="copies")
    internal_code = models.CharField(max_length=100, unique=True)
    state = models.CharField(max_length=20, choices=CopyState, default=CopyState.AVAILABLE)
    condition_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-condition_rating", "id"]

    def __str__(self):
        return self.internal_code
