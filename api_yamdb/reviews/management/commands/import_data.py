import csv

from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre, Review, Title,
                            TitleGenre, User)

TABLE_MODEL = {
    'category': Category,
    'comments': Comment,
    'genre_title': TitleGenre,
    'genre': Genre,
    'review': Review,
    'titles': Title,
    'users': User
}


class Command(BaseCommand):
    help = 'Импортирует в проект необходимые данные из csv-таблиц.'

    def handle(self, *args, **options):
        for table_name, model_name in TABLE_MODEL.items():
            with open(f'static/data/{table_name}.csv', newline='') as file:
                reader = csv.DictReader(file)
                objs = []
                for row in reader:
                    objs.append((model_name(**row)))
                model_name.objects.bulk_create(objs)

        self.stdout.write(self.style.SUCCESS('successfully printed table'))
