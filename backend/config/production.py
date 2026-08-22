import os

from .settings import *  # noqa: F403

DEBUG = False
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
ALLOWED_HOSTS = [host for host in os.environ["DJANGO_ALLOWED_HOSTS"].split(",") if host]
CORS_ALLOWED_ORIGINS = [
    origin for origin in os.environ["CORS_ALLOWED_ORIGINS"].split(",") if origin
]
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS
MAILERS = {"default": {"BACKEND": "django.core.mail.backends.smtp.EmailBackend"}}

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Strict"
X_FRAME_OPTIONS = "DENY"
