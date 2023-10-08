from django.contrib import admin

from .models import *

@admin.register(Article)
class ArticeAdmin(admin.ModelAdmin):
    list_display = "id", "title", "body", "published_at"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "name",

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = "name", "bio",
