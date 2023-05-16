from django.db import models
from .validators import validator_year
from django.contrib.auth.models import AbstractUser
from django.core.validators import (RegexValidator,
                                    MinValueValidator,
                                    MaxValueValidator)


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Адрес категории',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.TextField(
        verbose_name='Жанр',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Адрес жанра',
        max_length=50,
        unique=True

    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256
    )
    year = models.IntegerField(
        verbose_name='Год',
        validators=[validator_year],
        db_index=True
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


class User(AbstractUser):
    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        validators=[RegexValidator(regex=r"^[\w.@+-]",
                    message='Присутствуют недопустимые символы')],
    )
    email = models.EmailField(
        verbose_name='Почта',
        unique=True,
        max_length=254
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=len(MODERATOR),
        choices=ROLE_CHOICES,
        default=USER
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN

    def __str__(self):
        return self.username


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Произведение, к которуму написан отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    text = models.TextField(
        verbose_name='Отзыв'
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=(
            MinValueValidator(1, message='Оценка от 1 до 10'),
            MaxValueValidator(10, message='Оценка от 1 до 10')
        )
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата рецензии'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.text[:20]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Отзыв, к которуму написан комментарий'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(
        verbose_name='Коментарий'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:20]
