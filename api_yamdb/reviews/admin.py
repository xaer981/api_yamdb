from django.contrib import admin

from .models import Category, Genre, Title, TitleGenre


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    pass


@admin.register(TitleGenre)
class TitleGenreAdmin(admin.ModelAdmin):
    pass
