from django.contrib import admin
from .models import Category, Genre, Title, User, Review, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug'
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug'
    )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'year',
        'category'
    )
    filter_horizontal = ('genre',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'role',
        'email',
        'first_name',
        'last_name',
        'bio',
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'title',
        'author',
        'score',
        'pub_date'
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'review',
        'author',
        'pub_date'
    )
