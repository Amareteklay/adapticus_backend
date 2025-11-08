from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Post, Page

@admin.register(Post)
class PostAdmin(TranslatableAdmin):
    list_display = ("site","slug","status","published_at")
    list_filter = ("site","status","published_at")
    search_fields = ("translations__title","slug")
    ordering = ("-published_at",)

@admin.register(Page)
class PageAdmin(TranslatableAdmin):
    list_display = ("site","slug","is_home")
    list_filter = ("site","is_home")
    search_fields = ("translations__title","slug")
