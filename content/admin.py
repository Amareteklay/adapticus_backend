from django.contrib import admin
from django.utils.html import format_html
from parler.admin import TranslatableAdmin
from parler.utils.context import switch_language

from .models import Post, Page, PublishStatus
from core.models import MediaAsset, Author
from taxonomy.models import Tag, Category


@admin.register(Post)
class PostAdmin(TranslatableAdmin):
    list_display = ("title_localized", "site", "slug", "status", "published_at", "unlisted")
    list_filter = ("site", "status", "unlisted", "tags", "categories")
    search_fields = ("translations__title", "slug", "author__name")
    date_hierarchy = "published_at"
    ordering = ("-published_at",)
    autocomplete_fields = ("author", "hero_image", "tags", "categories")
    readonly_fields = ("created_at", "updated_at", "word_count")
    fieldsets = (
        ("Publishing", {
            "fields": ("site", "slug", "status", "published_at", "unlisted")
        }),
        ("Attribution & Media", {
            "fields": ("author", "hero_image", "reading_time_min", "word_count")
        }),
        ("Taxonomy", {
            "fields": ("tags", "categories")
        }),
        ("Meta", {
            "fields": ("meta", "created_at", "updated_at")
        }),
        ("Content (translations)", {
            "fields": ("title", "summary", "body_md", "seo_title", "seo_desc")
        }),
    )

    def title_localized(self, obj):
        # Show current admin language if available, fallback to any
        title = obj.safe_translation_getter("title", any_language=True) or obj.slug
        return title
    title_localized.short_description = "Title"


@admin.register(Page)
class PageAdmin(TranslatableAdmin):
    list_display = ("title_localized", "site", "slug", "is_home")
    list_filter = ("site", "is_home")
    search_fields = ("translations__title", "slug")
    ordering = ("site", "slug")
    autocomplete_fields = ("hero_image",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Basics", {
            "fields": ("site", "slug", "is_home", "hero_image")
        }),
        ("Meta", {
            "fields": ("meta", "created_at", "updated_at")
        }),
        ("Content (translations)", {
            "fields": ("title", "body_md", "seo_title", "seo_desc")
        }),
    )

    def title_localized(self, obj):
        return obj.safe_translation_getter("title", any_language=True) or obj.slug
    title_localized.short_description = "Title"
