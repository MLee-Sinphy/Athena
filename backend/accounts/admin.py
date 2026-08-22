from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class AthenaUserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = ("email", "registration_id", "role", "is_active", "is_staff")
    search_fields = ("email", "registration_id")
    fieldsets = (
        (None, {"fields": ("email", "registration_id", "password")}),
        ("Athena", {"fields": ("role", "must_change_password")}),
        ("Status", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Permissions", {"fields": ("groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at", "last_login")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "registration_id",
                    "role",
                    "password1",
                    "password2",
                    "must_change_password",
                ),
            },
        ),
    )
