from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.functions import Lower


class UserRole(models.TextChoices):
    READER = "reader", "Reader"
    ADMINISTRATOR = "administrator", "Administrator"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, registration_id, password=None, **extra_fields):
        if not email:
            raise ValueError("An email address is required.")
        if not registration_id:
            raise ValueError("A registration ID is required.")

        user = self.model(
            email=self.normalize_email(email),
            registration_id=registration_id,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, registration_id, password=None, **extra_fields):
        extra_fields.setdefault("role", UserRole.ADMINISTRATOR)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("must_change_password", False)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("A superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("A superuser must have is_superuser=True.")

        return self.create_user(email, registration_id, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    registration_id = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=20, choices=UserRole, default=UserRole.READER)
    must_change_password = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["registration_id"]

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("email"), name="accounts_user_email_ci_unique"),
        ]
        ordering = ["email"]

    def __str__(self):
        return self.email


class AccessToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="access_tokens")
    digest = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity_at = models.DateTimeField()
    absolute_expires_at = models.DateTimeField()
    revoked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["digest", "revoked_at"])]

    def __str__(self):
        return f"Token for {self.user_id}"
