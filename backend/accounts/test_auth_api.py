from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import SimpleTestCase, override_settings
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import AccessToken, UserRole


class AuthenticationApiTests(APITestCase):
    password = "a valid library passphrase"

    def setUp(self):
        cache.clear()
        self.user = get_user_model().objects.create_user(
            email="reader@example.com",
            registration_id="READER-001",
            password=self.password,
            must_change_password=False,
        )

    def login(self, identifier="reader@example.com", password=None):
        return self.client.post(
            "/api/v1/auth/login/",
            {"identifier": identifier, "password": password or self.password},
            format="json",
        )

    def authorize(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_email_and_registration_id_authenticate_with_same_shape(self):
        email_response = self.login()
        registration_response = self.login(identifier="READER-001")

        self.assertEqual(email_response.status_code, status.HTTP_200_OK)
        self.assertEqual(registration_response.status_code, status.HTTP_200_OK)
        self.assertEqual(email_response.data.keys(), registration_response.data.keys())
        self.assertIn("access_token", email_response.data)

    def test_invalid_credentials_do_not_reveal_whether_account_exists(self):
        unknown = self.login(identifier="missing@example.com", password="wrong password value")
        wrong_password = self.login(password="wrong password value")

        self.assertEqual(unknown.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(unknown.data, wrong_password.data)

    def test_only_a_digest_of_the_opaque_token_is_persisted(self):
        response = self.login()
        raw_token = response.data["access_token"]

        token = AccessToken.objects.get(user=self.user)
        self.assertNotEqual(token.digest, raw_token)
        self.assertNotIn(raw_token, token.digest)

    def test_authenticated_user_can_read_own_profile_and_logout(self):
        raw_token = self.login().data["access_token"]
        self.authorize(raw_token)

        profile = self.client.get("/api/v1/auth/me/")
        logout = self.client.post("/api/v1/auth/logout/")
        rejected = self.client.get("/api/v1/auth/me/")

        self.assertEqual(profile.status_code, status.HTTP_200_OK)
        self.assertEqual(profile.data["email"], self.user.email)
        self.assertEqual(logout.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(rejected.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_inactive_and_absolute_session_limits_are_enforced(self):
        first = self.login().data["access_token"]
        first_record = AccessToken.objects.latest("created_at")
        AccessToken.objects.filter(pk=first_record.pk).update(
            last_activity_at=timezone.now() - timedelta(minutes=31)
        )
        self.authorize(first)
        self.assertEqual(self.client.get("/api/v1/auth/me/").status_code, 401)

        self.client.credentials()
        second = self.login().data["access_token"]
        second_record = AccessToken.objects.latest("created_at")
        AccessToken.objects.filter(pk=second_record.pk).update(
            absolute_expires_at=timezone.now() - timedelta(seconds=1)
        )
        self.authorize(second)
        self.assertEqual(self.client.get("/api/v1/auth/me/").status_code, 401)

    def test_changing_email_validates_uniqueness(self):
        get_user_model().objects.create_user(
            email="other@example.com",
            registration_id="READER-002",
            password=self.password,
        )
        self.authorize(self.login().data["access_token"])

        conflict = self.client.patch(
            "/api/v1/auth/me/", {"email": "OTHER@example.com"}, format="json"
        )

        self.assertEqual(conflict.status_code, status.HTTP_400_BAD_REQUEST)


class FirstAccessAndRecoveryTests(APITestCase):
    old_password = "a temporary library passphrase"
    new_password = "a permanent library passphrase"

    def setUp(self):
        cache.clear()
        self.user = get_user_model().objects.create_user(
            email="first@example.com",
            registration_id="FIRST-001",
            password=self.old_password,
        )

    def login(self, user, password):
        return self.client.post(
            "/api/v1/auth/login/",
            {"identifier": user.email, "password": password},
            format="json",
        )

    def authorize(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_temporary_password_blocks_common_endpoint_until_changed(self):
        token = self.login(self.user, self.old_password).data["access_token"]
        self.authorize(token)

        blocked = self.client.get("/api/v1/auth/me/")
        changed = self.client.post(
            "/api/v1/auth/password/change/",
            {"current_password": self.old_password, "new_password": self.new_password},
            format="json",
        )
        old_session = self.client.get("/api/v1/auth/me/")

        self.assertEqual(blocked.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(blocked.data["code"], "password_change_required")
        self.assertEqual(changed.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(old_session.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.login(self.user, self.new_password).status_code, 200)

    def test_reader_cannot_reset_password_but_administrator_can_and_revokes_sessions(self):
        self.user.must_change_password = False
        self.user.save(update_fields=["must_change_password"])
        user_token = self.login(self.user, self.old_password).data["access_token"]
        self.authorize(user_token)
        forbidden = self.client.post(
            f"/api/v1/admin/users/{self.user.pk}/reset-password/",
            {"temporary_password": "a replacement temporary phrase"},
            format="json",
        )

        admin = get_user_model().objects.create_superuser(
            email="admin@example.com",
            registration_id="ADMIN-001",
            password="an administrative passphrase",
        )
        self.client.credentials()
        self.authorize(self.login(admin, "an administrative passphrase").data["access_token"])
        reset = self.client.post(
            f"/api/v1/admin/users/{self.user.pk}/reset-password/",
            {"temporary_password": "a replacement temporary phrase"},
            format="json",
        )

        self.assertEqual(forbidden.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(reset.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            AccessToken.objects.filter(user=self.user, revoked_at__isnull=True).exists()
        )
        self.user.refresh_from_db()
        self.assertTrue(self.user.must_change_password)

    def test_only_administrator_can_create_a_reader_with_temporary_password(self):
        admin = get_user_model().objects.create_superuser(
            email="admin-create@example.com",
            registration_id="ADMIN-002",
            password="an administrative passphrase",
        )
        reader_token = self.login(self.user, self.old_password).data["access_token"]
        self.authorize(reader_token)
        payload = {
            "email": "new-reader@example.com",
            "registration_id": "NEW-001",
            "temporary_password": "a new temporary passphrase",
        }
        forbidden = self.client.post("/api/v1/admin/users/", payload, format="json")

        self.client.credentials()
        self.authorize(self.login(admin, "an administrative passphrase").data["access_token"])
        created = self.client.post("/api/v1/admin/users/", payload, format="json")

        self.assertEqual(forbidden.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        new_reader = get_user_model().objects.get(registration_id="NEW-001")
        self.assertEqual(new_reader.role, UserRole.READER)
        self.assertTrue(new_reader.must_change_password)
        self.assertTrue(new_reader.check_password(payload["temporary_password"]))

    def test_reader_role_cannot_be_supplied_by_client_as_administrator(self):
        self.user.must_change_password = False
        self.user.save(update_fields=["must_change_password"])
        token = self.login(self.user, self.old_password).data["access_token"]
        self.authorize(token)

        response = self.client.patch(
            "/api/v1/auth/me/", {"role": UserRole.ADMINISTRATOR}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, UserRole.READER)

    def test_login_attempts_are_rate_limited(self):
        for _ in range(5):
            self.login(self.user, "wrong password value")

        response = self.login(self.user, "wrong password value")
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


@override_settings(CORS_ALLOWED_ORIGINS=["https://mlee-sinphy.github.io"])
class CorsPolicyTests(SimpleTestCase):
    def test_allowed_frontend_origin_receives_cors_header(self):
        response = self.client.options(
            "/api/v1/auth/login/", headers={"origin": "https://mlee-sinphy.github.io"}
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response["Access-Control-Allow-Origin"], "https://mlee-sinphy.github.io")

    def test_unknown_origin_receives_no_cors_permission(self):
        response = self.client.options(
            "/api/v1/auth/login/", headers={"origin": "https://untrusted.example"}
        )

        self.assertNotIn("Access-Control-Allow-Origin", response)
