import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title, Review, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        with open(f'{settings.BASE_DIR}/static/data/category.csv') as cvs_file:
            file_reader = csv.DictReader(cvs_file)
            for row in file_reader:
                db = Category(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                db.save()

        with open(f'{settings.BASE_DIR}/static/data/genre.csv') as cvs_file:
            file_reader = csv.DictReader(cvs_file)
            for row in file_reader:
                db = Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                db.save()

        with open(f'{settings.BASE_DIR}/static/data/users.csv') as cvs_file:
            file_reader = csv.DictReader(cvs_file)
            for row in file_reader:
                db = User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )
                db.save()

        with open(f'{settings.BASE_DIR}/static/data/titles.csv') as cvs_file:
            file_reader = csv.DictReader(cvs_file)
            for row in file_reader:
                db = Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category']
                )
                db.save()

        with open(f'{settings.BASE_DIR}/static/data/review.csv') as cvs_file:
            file_reader = csv.DictReader(cvs_file)
            for row in file_reader:
                db = Review(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author_id=row['author'],
                    score=row['score'],
                    pub_date=row['pub_date']

                )
                db.save()

        with open(f'{settings.BASE_DIR}/static/data/comments.csv') as cvs_file:
            file_reader = csv.DictReader(cvs_file)
            for row in file_reader:
                db = Comment(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author_id=row['author'],
                    pub_date=row['pub_date']
                )
                db.save()

        print('База данных скачана')
