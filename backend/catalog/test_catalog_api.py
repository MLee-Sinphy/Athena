from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from accounts.authentication import issue_token
from catalog.models import BookCopy, BookTitle, CopyState, Tag


class CatalogApiTests(TestCase):
    def setUp(self):
        self.reader = get_user_model().objects.create_user(
            email="reader-catalog@example.com",
            registration_id="CATALOG-001",
            password="a valid library passphrase",
            must_change_password=False,
        )
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {issue_token(self.reader)}")
        self.title = BookTitle.objects.create(
            name="O Nome da Rosa",
            author="Umberto Eco",
            publisher="Record",
            edition="1ª edição",
            publication_year=1980,
            category="Mistério histórico",
            description="Um mistério medieval investigado em uma abadia.",
            cover="covers/name-of-the-rose.jpg",
        )
        self.title.tags.add(Tag.objects.create(name="medieval"))
        BookCopy.objects.create(
            title=self.title,
            internal_code="COPY-SECRET-001",
            state=CopyState.AVAILABLE,
            condition_rating=5,
        )
        BookCopy.objects.create(
            title=self.title,
            internal_code="COPY-SECRET-002",
            state=CopyState.AVAILABLE,
            condition_rating=3,
        )

    def test_catalog_groups_copies_under_one_title_without_internal_codes(self):
        response = self.client.get("/api/v1/catalog/titles/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        item = response.data["results"][0]
        self.assertEqual(item["available_copies"], 2)
        self.assertNotIn("internal_code", str(item))

    def test_reader_can_compare_available_copies_only_by_condition(self):
        response = self.client.get(f"/api/v1/catalog/titles/{self.title.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual([copy["condition_rating"] for copy in response.data["copies"]], [5, 3])
        self.assertNotIn("COPY-SECRET", str(response.data))

    def test_search_finds_description_and_hash_tag(self):
        by_description = self.client.get("/api/v1/catalog/titles/?q=abadia")
        by_tag = self.client.get("/api/v1/catalog/titles/?q=%23medieval")

        self.assertEqual(len(by_description.data["results"]), 1)
        self.assertEqual(len(by_tag.data["results"]), 1)

    def test_catalog_limits_page_size_for_large_collections(self):
        BookTitle.objects.bulk_create(
            [
                BookTitle(
                    name=f"Livro {index}",
                    author="Autoria de teste",
                    publisher="Editora de teste",
                    edition="1ª edição",
                    publication_year=2020,
                    category="Teste",
                    description="Volume sintético para validar paginação.",
                    cover=f"covers/{index}.jpg",
                )
                for index in range(101)
            ]
        )

        response = self.client.get("/api/v1/catalog/titles/?page_size=500")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 102)
        self.assertEqual(len(response.data["results"]), 100)
        self.assertIsNotNone(response.data["next"])

    def test_isbn_and_page_count_are_optional(self):
        title = BookTitle.objects.create(
            name="Livro sem ISBN",
            author="Autora Exemplo",
            publisher="Editora Exemplo",
            edition="1ª edição",
            publication_year=2020,
            category="Ensaios",
            description="Uma descrição suficiente.",
            cover="covers/example.jpg",
        )

        self.assertEqual(title.isbn, "")
        self.assertIsNone(title.page_count)


class LoadDataCommandTests(TestCase):
    def test_command_creates_requested_synthetic_volume(self):
        call_command("seed_load_data", readers=2, titles=3, copies=5, verbosity=0)

        self.assertEqual(
            get_user_model().objects.filter(registration_id__startswith="LOAD-").count(), 2
        )
        self.assertEqual(BookTitle.objects.filter(name__startswith="Volume sintético").count(), 3)
        self.assertEqual(BookCopy.objects.filter(internal_code__startswith="LOAD-COPY-").count(), 5)


class DemoDataCommandTests(TestCase):
    @override_settings(MEDIA_ROOT="/tmp/athena-test-demo-media")
    def test_command_is_idempotent_and_creates_known_profiles_and_collection(self):
        with patch.dict("os.environ", {"ATHENA_DEMO_PASSWORD": "Valid-demo-passphrase!42"}):
            call_command("seed_demo_data", verbosity=0)
            call_command("seed_demo_data", verbosity=0)

        admin = get_user_model().objects.get(email="mlee.admin@proton.me")
        self.assertEqual(admin.whatsapp_number, "+5500000000001")
        student = get_user_model().objects.get(email="mlee.student@proton.me")
        self.assertEqual(admin.registration_id, "ADM-001")
        self.assertEqual(admin.role, "administrator")
        self.assertEqual(student.registration_id, "ALU-000001")
        self.assertEqual(student.whatsapp_number, "+5500000000002")
        self.assertEqual(student.role, "reader")
        self.assertTrue(admin.check_password("Valid-demo-passphrase!42"))
        self.assertTrue(student.check_password("Valid-demo-passphrase!42"))
        self.assertEqual(
            BookTitle.objects.filter(publisher="Edição demonstrativa Athena").count(), 8
        )
        self.assertEqual(BookCopy.objects.filter(internal_code__startswith="DEMO-").count(), 25)


class CatalogAdministrationTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            email="catalog-admin@example.com",
            registration_id="CATALOG-ADMIN",
            password="an administrative passphrase",
        )
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {issue_token(self.admin)}")

    def test_administrator_creates_title_and_uniquely_identified_copies(self):
        title_response = self.client.post(
            "/api/v1/admin/catalog/titles/",
            {
                "name": "Dom Casmurro",
                "author": "Machado de Assis",
                "publisher": "Garnier",
                "edition": "1ª edição",
                "publication_year": 1899,
                "category": "Romance",
                "description": "Um clássico da literatura brasileira.",
                "cover": SimpleUploadedFile("cover.jpg", b"\xff\xd8\xff\xe0valid", "image/jpeg"),
            },
            format="multipart",
        )
        copy_response = self.client.post(
            "/api/v1/admin/catalog/copies/",
            {"title": title_response.data["id"], "internal_code": "DOM-001", "condition_rating": 4},
            format="json",
        )

        self.assertEqual(title_response.status_code, 201)
        self.assertEqual(copy_response.status_code, 201)

    def test_invalid_cover_upload_is_rejected(self):
        response = self.client.post(
            "/api/v1/admin/catalog/titles/",
            {
                "name": "Arquivo inválido",
                "author": "Autora",
                "publisher": "Editora",
                "edition": "1",
                "publication_year": 2024,
                "category": "Teste",
                "description": "Este arquivo não é uma imagem.",
                "cover": SimpleUploadedFile("attack.html", b"<script>bad()</script>", "text/html"),
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 400)

    def test_valid_cover_is_available_only_to_authenticated_users(self):
        title_response = self.client.post(
            "/api/v1/admin/catalog/titles/",
            {
                "name": "Capa protegida",
                "author": "Autora",
                "publisher": "Editora",
                "edition": "1",
                "publication_year": 2024,
                "category": "Teste",
                "description": "Uma imagem válida para o teste.",
                "cover": SimpleUploadedFile("valid.jpg", b"\xff\xd8\xff\xe0valid", "image/jpeg"),
            },
            format="multipart",
        )
        title_id = title_response.data["id"]
        catalog_response = self.client.get(f"/api/v1/catalog/titles/{title_id}/")
        media_path = catalog_response.data["cover"].split("testserver", 1)[1]

        authorized = self.client.get(media_path)
        self.client.credentials()
        anonymous = self.client.get(media_path)

        self.assertEqual(authorized.status_code, 200)
        self.assertEqual(anonymous.status_code, 401)

    def test_reader_cannot_use_catalog_administration(self):
        reader = get_user_model().objects.create_user(
            email="forbidden@example.com",
            registration_id="FORBIDDEN-001",
            password="a valid library passphrase",
            must_change_password=False,
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {issue_token(reader)}")

        response = self.client.post("/api/v1/admin/catalog/copies/", {}, format="json")

        self.assertEqual(response.status_code, 403)

    def test_administrator_updates_title_tags_and_restores_copy_state(self):
        title = BookTitle.objects.create(
            name="Estado inicial",
            author="Autora",
            publisher="Editora",
            edition="1",
            publication_year=2024,
            category="Teste",
            description="Descrição inicial.",
            cover="covers/existing.jpg",
        )
        copy = BookCopy.objects.create(
            title=title, internal_code="RESTORE-001", state=CopyState.LOST, condition_rating=2
        )

        title_response = self.client.patch(
            f"/api/v1/admin/catalog/titles/{title.pk}/",
            {"name": "Estado atualizado", "tag_names": ["academia"]},
            format="json",
        )
        copy_response = self.client.patch(
            f"/api/v1/admin/catalog/copies/{copy.pk}/",
            {"state": CopyState.AVAILABLE},
            format="json",
        )

        self.assertEqual(title_response.status_code, 200)
        self.assertEqual(copy_response.status_code, 200)
        self.assertTrue(title.tags.filter(name="academia").exists())
        copy.refresh_from_db()
        self.assertEqual(copy.state, CopyState.AVAILABLE)

    def test_duplicate_internal_copy_code_is_rejected(self):
        title = BookTitle.objects.create(
            name="Duplicado",
            author="Autora",
            publisher="Editora",
            edition="1",
            publication_year=2024,
            category="Teste",
            description="Descrição.",
            cover="covers/existing.jpg",
        )
        BookCopy.objects.create(title=title, internal_code="UNIQUE-001", condition_rating=4)

        response = self.client.post(
            "/api/v1/admin/catalog/copies/",
            {"title": title.pk, "internal_code": "UNIQUE-001", "condition_rating": 3},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_administrator_adds_optional_book_image(self):
        title = BookTitle.objects.create(
            name="Com imagem",
            author="Autora",
            publisher="Editora",
            edition="1",
            publication_year=2024,
            category="Teste",
            description="Descrição.",
            cover="covers/existing.jpg",
        )

        response = self.client.post(
            "/api/v1/admin/catalog/images/",
            {
                "title": title.pk,
                "alt_text": "Contracapa",
                "image": SimpleUploadedFile("back.png", b"\x89PNG\r\n\x1a\nvalid", "image/png"),
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(title.additional_images.count(), 1)
