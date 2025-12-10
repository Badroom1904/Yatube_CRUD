import csv
import os

from django.core.management.base import BaseCommand
from django.conf import settings

from reviews.models import Category, Genre, Title, GenreTitle


class Command(BaseCommand):
    help = 'Импорт данных из CSV файлов в базу данных'

    def handle(self, *args, **options):
        data_path = os.path.join(settings.BASE_DIR, 'static', 'data')
        self.stdout.write('Начинаем импорт данных...')

        # 1. Импорт категорий
        self._import_categories(data_path)

        # 2. Импорт жанров
        self._import_genres(data_path)

        # 3. Импорт произведений
        self._import_titles(data_path)

        # 4. Импорт связей жанр-произведение
        self._import_genre_titles(data_path)

        self.stdout.write(self.style.SUCCESS(
            'Импорт данных завершен успешно!'))

    def _import_categories(self, data_path):
        """Импорт категорий."""
        file_path = os.path.join(data_path, 'category.csv')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(
                'Файл category.csv не найден'))
            return

        with open(file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            categories = []

            for row in reader:
                categories.append(Category(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                ))

            Category.objects.bulk_create(categories, ignore_conflicts=True)
            self.stdout.write(f'Импортировано {len(categories)} категорий')

    def _import_genres(self, data_path):
        """Импорт жанров."""
        file_path = os.path.join(data_path, 'genre.csv')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING('Файл genre.csv не найден'))
            return

        with open(file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            genres = []

            for row in reader:
                genres.append(Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                ))

            Genre.objects.bulk_create(genres, ignore_conflicts=True)
            self.stdout.write(f'Импортировано {len(genres)} жанров')

    def _import_titles(self, data_path):
        """Импорт произведений."""
        file_path = os.path.join(data_path, 'titles.csv')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING('Файл titles.csv не найден'))
            return

        with open(file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            titles = []

            for row in reader:
                # Проверяем и преобразуем year
                try:
                    year = int(row['year']) if row['year'] else None
                except ValueError:
                    year = None
                    self.stdout.write(self.style.WARNING(
                        f'Неверный год: {row["year"]}'))

                titles.append(Title(
                    id=row['id'],
                    name=row['name'],
                    year=year,
                    category_id=row['category'] if row['category'] else None,
                    description=row.get('description', '')
                ))

            Title.objects.bulk_create(titles, ignore_conflicts=True)
            self.stdout.write(f'Импортировано {len(titles)} произведений')

    def _import_genre_titles(self, data_path):
        """Импорт связей жанр-произведение."""
        file_path = os.path.join(data_path, 'genre_title.csv')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(
                'Файл genre_title.csv не найден'))
            return

        with open(file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            genre_titles = []

            for row in reader:
                genre_titles.append(GenreTitle(
                    id=row['id'],
                    title_id=row['title_id'],
                    genre_id=row['genre_id']
                ))

            GenreTitle.objects.bulk_create(genre_titles, ignore_conflicts=True)
            self.stdout.write(
                f'Импортировано {len(genre_titles)} связей жанр-произведение')
