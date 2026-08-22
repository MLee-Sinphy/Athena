import hashlib
import secrets
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from .models import AccessToken


def token_digest(raw_token):
    return hashlib.sha256(raw_token.encode()).hexdigest()


def issue_token(user):
    raw_token = secrets.token_urlsafe(32)
    now = timezone.now()
    AccessToken.objects.create(
        user=user,
        digest=token_digest(raw_token),
        last_activity_at=now,
        absolute_expires_at=now + timedelta(hours=settings.AUTH_TOKEN_ABSOLUTE_HOURS),
    )
    return raw_token


def revoke_user_tokens(user):
    user.access_tokens.filter(revoked_at__isnull=True).update(revoked_at=timezone.now())


class OpaqueTokenAuthentication(BaseAuthentication):
    keyword = b"Bearer"

    def authenticate(self, request):
        parts = get_authorization_header(request).split()
        if not parts:
            return None
        if len(parts) != 2 or parts[0] != self.keyword:
            raise AuthenticationFailed("Invalid authentication credentials.")

        try:
            raw_token = parts[1].decode()
            token = AccessToken.objects.select_related("user").get(
                digest=token_digest(raw_token), revoked_at__isnull=True
            )
        except (UnicodeDecodeError, AccessToken.DoesNotExist):
            raise AuthenticationFailed("Invalid authentication credentials.") from None

        now = timezone.now()
        inactivity_limit = now - timedelta(minutes=settings.AUTH_TOKEN_INACTIVITY_MINUTES)
        if token.last_activity_at < inactivity_limit or token.absolute_expires_at <= now:
            token.revoked_at = now
            token.save(update_fields=["revoked_at"])
            raise AuthenticationFailed("Invalid authentication credentials.")
        if not token.user.is_active:
            raise AuthenticationFailed("Invalid authentication credentials.")

        token.last_activity_at = now
        token.save(update_fields=["last_activity_at"])
        return token.user, token

    def authenticate_header(self, request):
        return "Bearer"
