import json
import os
import time
import urllib.parse
import urllib.request

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.management.base import BaseCommand, CommandError

from accounts.models import UserRole
from catalog.models import BookCopy, BookTitle, Tag

BOOKS = (
    (
        "9780720608458",
        "Dom Casmurro",
        "Machado de Assis",
        1899,
        "Romance",
        ("brasil", "clássico", "memória"),
        3,
    ),
    (
        "9786559570737",
        "O Pequeno Príncipe",
        "Antoine de Saint-Exupéry",
        1943,
        "Fábula",
        ("amizade", "infância", "filosofia"),
        3,
    ),
    (
        "9780451524935",
        "1984",
        "George Orwell",
        1949,
        "Ficção distópica",
        ("distopia", "política", "sociedade"),
        4,
    ),
    (
        "9780156001311",
        "O Nome da Rosa",
        "Umberto Eco",
        1980,
        "Mistério histórico",
        ("mistério", "medieval", "investigação"),
        3,
    ),
    (
        "9781546765912",
        "Frankenstein",
        "Mary Shelley",
        1818,
        "Ficção gótica",
        ("gótico", "ciência", "clássico"),
        2,
    ),
    (
        "9788533615540",
        "O Hobbit",
        "J. R. R. Tolkien",
        1937,
        "Fantasia",
        ("fantasia", "aventura", "medieval"),
        4,
    ),
    (
        "9786580309313",
        "Torto Arado",
        "Itamar Vieira Junior",
        2019,
        "Romance brasileiro",
        ("brasil", "memória", "sociedade"),
        3,
    ),
    (
        "9786555790641",
        "A Revolução dos Bichos",
        "George Orwell",
        1945,
        "Sátira",
        ("política", "fábula", "clássico"),
        3,
    ),
)


class Command(BaseCommand):
    help = "Create idempotent fictional demo accounts and a realistic book collection."

    def add_arguments(self, parser):
        parser.add_argument("--enrich-open-library", action="store_true")

    def handle(self, *args, **options):
        password = os.environ.get("ATHENA_DEMO_PASSWORD", "")
        if not password:
            raise CommandError("ATHENA_DEMO_PASSWORD is required.")
        try:
            validate_password(password)
        except Exception as error:
            raise CommandError("ATHENA_DEMO_PASSWORD must satisfy the password policy.") from error

        user_model = get_user_model()
        accounts = (
            ("mlee.admin@proton.me", "ADM-001", UserRole.ADMINISTRATOR),
            ("mlee.student@proton.me", "ALU-000001", UserRole.READER),
        )
        for email, registration_id, role in accounts:
            user, _ = user_model.objects.update_or_create(
                email=email,
                defaults={
                    "registration_id": registration_id,
                    "role": role,
                    "must_change_password": False,
                    "is_active": True,
                    "is_staff": role == UserRole.ADMINISTRATOR,
                },
            )
            user.set_password(password)
            user.save(update_fields=["password", "updated_at"])

        for index, (isbn, name, author, year, category, tag_names, copies) in enumerate(BOOKS):
            metadata = self.open_library_metadata(isbn) if options["enrich_open_library"] else {}
            title, _ = BookTitle.objects.update_or_create(
                isbn=isbn,
                defaults={
                    "name": name,
                    "author": author,
                    "publisher": (metadata.get("publisher") or "Edição demonstrativa Athena")[:255],
                    "edition": "1ª edição",
                    "publication_year": metadata.get("publication_year") or year,
                    "category": (metadata.get("category") or category)[:120],
                    "description": (
                        f"Uma obra de {author} disponível para explorar no catálogo "
                        "demonstrativo da Athena."
                    ),
                    "cover": "",
                    "page_count": metadata.get("page_count"),
                    "metadata_source_url": metadata.get("source_url", ""),
                },
            )
            combined_tags = (*tag_names, *metadata.get("tags", ()))
            title.tags.set(
                Tag.objects.get_or_create(name=tag[:80].strip().lower())[0]
                for tag in combined_tags
                if tag.strip()
            )
            for copy_index in range(1, copies + 1):
                BookCopy.objects.update_or_create(
                    internal_code=f"DEMO-{index + 1:03d}-{copy_index:02d}",
                    defaults={"title": title, "condition_rating": 2 + copy_index % 4},
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo ready: {len(accounts)} accounts, {len(BOOKS)} titles and "
                f"{sum(book[-1] for book in BOOKS)} copies."
            )
        )

    def open_library_metadata(self, isbn):
        query = urllib.parse.urlencode(
            {
                "q": f"isbn:{isbn}",
                "fields": (
                    "key,title,author_name,publisher,first_publish_year,subject,"
                    "number_of_pages_median"
                ),
                "limit": 1,
            }
        )
        request = urllib.request.Request(
            f"https://openlibrary.org/search.json?{query}",
            headers={"User-Agent": "AthenaLibrary/1.0 (mlee.contact@proton.me)"},
        )
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                documents = json.load(response).get("docs", [])
            time.sleep(1.05)
        except (OSError, ValueError) as error:
            self.stderr.write(self.style.WARNING(f"Open Library unavailable for {isbn}: {error}"))
            return {}
        if not documents:
            return {}
        document = documents[0]
        return {
            "title": document.get("title"),
            "author": ", ".join(document.get("author_name", [])[:3]),
            "publisher": next(iter(document.get("publisher", [])), ""),
            "publication_year": document.get("first_publish_year"),
            "category": next(iter(document.get("subject", [])), ""),
            "page_count": document.get("number_of_pages_median"),
            "tags": tuple(document.get("subject", [])[:5]),
            "source_url": f"https://openlibrary.org{document['key']}"
            if document.get("key")
            else "",
        }
