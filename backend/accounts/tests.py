from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import UserRole


class UserModelTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()

    def test_reader_is_created_with_normalized_unique_identity(self):
        user = self.user_model.objects.create_user(
            email="Reader@Example.COM",
            registration_id="STUDENT-001",
            password="a sufficiently long passphrase",
        )

        self.assertEqual(user.email, "Reader@example.com")
        self.assertEqual(user.registration_id, "STUDENT-001")
        self.assertEqual(user.role, UserRole.READER)
        self.assertTrue(user.must_change_password)
        self.assertTrue(user.check_password("a sufficiently long passphrase"))
        self.assertNotEqual(user.password, "a sufficiently long passphrase")

    def test_email_is_unique_case_insensitively(self):
        self.user_model.objects.create_user(
            email="reader@example.com",
            registration_id="STUDENT-001",
            password="a sufficiently long passphrase",
        )

        with self.assertRaises(IntegrityError), transaction.atomic():
            self.user_model.objects.create_user(
                email="READER@example.com",
                registration_id="STUDENT-002",
                password="another sufficiently long passphrase",
            )

    def test_registration_id_is_unique(self):
        self.user_model.objects.create_user(
            email="first@example.com",
            registration_id="STUDENT-001",
            password="a sufficiently long passphrase",
        )

        with self.assertRaises(IntegrityError), transaction.atomic():
            self.user_model.objects.create_user(
                email="second@example.com",
                registration_id="STUDENT-001",
                password="another sufficiently long passphrase",
            )

    def test_superuser_has_administrator_role(self):
        user = self.user_model.objects.create_superuser(
            email="admin@example.com",
            registration_id="ADMIN-001",
            password="an administrative passphrase",
        )

        self.assertEqual(user.role, UserRole.ADMINISTRATOR)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class PasswordPolicyTests(TestCase):
    def test_password_shorter_than_fifteen_characters_is_rejected(self):
        with self.assertRaises(ValidationError):
            validate_password("short password")

    def test_common_password_is_rejected(self):
        with self.assertRaises(ValidationError):
            validate_password("passwordpassword")

    def test_long_passphrase_is_accepted_without_composition_rules(self):
        validate_password("a calm library phrase with spaces")
