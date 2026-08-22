from django.urls import path

from .views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    ProfileView,
    ReaderCreateView,
)

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/me/", ProfileView.as_view(), name="profile"),
    path("auth/password/change/", PasswordChangeView.as_view(), name="password-change"),
    path("admin/users/", ReaderCreateView.as_view(), name="reader-create"),
    path(
        "admin/users/<int:user_id>/reset-password/",
        PasswordResetView.as_view(),
        name="password-reset",
    ),
]
