from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from catalog.models import BookCopy, BookTitle


class Command(BaseCommand):
    help = "Create an isolated synthetic data set for the documented load test."

    def add_arguments(self, parser):
        parser.add_argument("--readers", type=int, default=5_000)
        parser.add_argument("--titles", type=int, default=20_000)
        parser.add_argument("--copies", type=int, default=50_000)

    def handle(self, *args, **options):
        readers = options["readers"]
        title_count = options["titles"]
        copy_count = options["copies"]
        if min(readers, title_count, copy_count) < 1 or copy_count < title_count:
            raise CommandError("Counts must be positive and copies must cover every title.")
        if get_user_model().objects.filter(registration_id__startswith="LOAD-").exists():
            raise CommandError("Synthetic LOAD-* records already exist; use a fresh database.")

        user_model = get_user_model()
        user_model.objects.bulk_create(
            [
                user_model(
                    email=f"load-reader-{index}@example.invalid",
                    registration_id=f"LOAD-{index:06d}",
                    password="!",
                    must_change_password=False,
                )
                for index in range(readers)
            ],
            batch_size=1_000,
        )
        titles = BookTitle.objects.bulk_create(
            [
                BookTitle(
                    name=f"Volume sintético {index:06d}",
                    author=f"Autor {index % 500:03d}",
                    publisher="Editora de carga",
                    edition="1ª edição",
                    publication_year=2000 + index % 25,
                    category=f"Categoria {index % 20:02d}",
                    description="Registro sintético sem dado pessoal para ensaio de carga.",
                    cover=f"covers/load-{index:06d}.jpg",
                )
                for index in range(title_count)
            ],
            batch_size=1_000,
        )
        BookCopy.objects.bulk_create(
            [
                BookCopy(
                    title=titles[index % title_count],
                    internal_code=f"LOAD-COPY-{index:07d}",
                    condition_rating=1 + index % 5,
                )
                for index in range(copy_count)
            ],
            batch_size=1_000,
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {readers} readers, {title_count} titles and {copy_count} copies."
            )
        )
