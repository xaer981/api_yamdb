import csv

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from reviews.models import (Category, Comment, Genre, Review, Title,
                            TitleGenre, User)

TABLE_MODEL = {
    'users': User,
    'category': Category,
    'genre': Genre,
    'titles': Title,
    'review': Review,
    'comments': Comment,
    'genre_title': TitleGenre,
}


class Command(BaseCommand):
    """
    Импортирует данные из CSV-таблиц.
    При обнаружении дубликата/некорректной записи(нет необходимых полей),
    игнорирует конкретную запись и продолжает импорт дальше.
    """
    help = 'Импортирует в проект необходимые данные из csv-таблиц.'

    def get_obj_from_db(self, row):
        """
        Функция для получения
        существующего объекта User или Category из БД.
        """
        message = '{} c id {} не существует.'

        if author_id := row.get('author'):
            try:
                row['author'] = User.objects.get(pk=author_id)
            except User.DoesNotExist:
                raise CommandError(message.format('User', author_id))

        if category_id := row.get('category'):
            try:
                row['category'] = Category.objects.get(pk=category_id)
            except Category.DoesNotExist:
                raise CommandError(message.format('Category', category_id))

        return row

    def handle(self, *args, **options):
        """Сами действия при запуске команды."""
        self.stdout.write(self.style.NOTICE('Импорт начался, ожидайте...'))
        self.stdout.write(self.style.NOTICE('============================='))
        for table_name, model_name in TABLE_MODEL.items():
            with open(f'static/data/{table_name}.csv',
                      newline='',
                      encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    if any([row.get('author'), row.get('category')]):
                        row = self.get_obj_from_db(row)

                    try:
                        model_name.objects.create(**row)
                    except IntegrityError:
                        continue

        self.stdout.write(self.style.SUCCESS(
            'Данные успешно импортированы!'))
