# content/serializers.py
from __future__ import annotations

from rest_framework import serializers
from parler.utils.context import switch_language

from .models import Post, Page
from core.models import MediaAsset, Author
from .markdown import md_to_html
from .utils import DEFAULT_LANG


def _media_url(asset: MediaAsset | None) -> str | None:
    if not asset:
        return None
    try:
        return asset.file.url
    except Exception:
        return None


class MediaAssetMini(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = MediaAsset
        fields = (
            "id",
            "kind",
            "url",
            "width",
            "height",
            "duration_ms",
            "alt_text",
            "caption",
            "meta",
        )

    def get_url(self, obj: MediaAsset) -> str | None:
        return _media_url(obj)


class AuthorMini(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ("id", "name", "slug", "url", "avatar_url")

    def get_avatar_url(self, obj: Author) -> str | None:
        return _media_url(obj.avatar)


class BaseTranslatedSerializer(serializers.ModelSerializer):
    """
    Parler-aware base serializer that flattens active translation into:
      - title, summary (if present), body_html, seo_title, seo_desc
    Also returns:
      - active_locale, available_locales
      - hero_image_data (mini)
    """

    # i18n/meta
    active_locale = serializers.SerializerMethodField()
    available_locales = serializers.SerializerMethodField()

    # flattened translation fields
    title = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()   # present on Post; for Page returns ""
    body_html = serializers.SerializerMethodField()
    seo_title = serializers.SerializerMethodField()
    seo_desc = serializers.SerializerMethodField()

    # media
    hero_image_data = serializers.SerializerMethodField()

    # helpers
    def _lang(self) -> str:
        return self.context.get("lang", DEFAULT_LANG)

    def _with_lang(self, obj):
        # parler context manager
        return switch_language(obj, self._lang())

    # meta
    def get_active_locale(self, obj) -> str:
        return self._lang()

    def get_available_locales(self, obj) -> list[str]:
        try:
            return obj.get_available_languages()
        except Exception:
            return []

    # flattened fields
    def get_title(self, obj) -> str:
        with self._with_lang(obj):
            return getattr(obj, "title", "") or getattr(obj, "slug", "")

    def get_summary(self, obj) -> str:
        # For Page this returns "" because 'summary' doesn't exist there
        with self._with_lang(obj):
            return getattr(obj, "summary", "") or ""

    def get_body_html(self, obj) -> str:
        with self._with_lang(obj):
            return md_to_html(getattr(obj, "body_md", ""))

    def get_seo_title(self, obj) -> str:
        with self._with_lang(obj):
            return getattr(obj, "seo_title", "") or self.get_title(obj)

    def get_seo_desc(self, obj) -> str:
        with self._with_lang(obj):
            return getattr(obj, "seo_desc", "") or ""

    # media
    def get_hero_image_data(self, obj) -> dict | None:
        asset = getattr(obj, "hero_image", None)
        return MediaAssetMini(asset).data if asset else None


class PublicPostSerializer(BaseTranslatedSerializer):
    author = AuthorMini(read_only=True)
    tags = serializers.SlugRelatedField(slug_field="slug", many=True, read_only=True)
    categories = serializers.SlugRelatedField(slug_field="slug", many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            # identity & state
            "id",
            "site",
            "slug",
            "status",
            "published_at",
            "unlisted",
            # relations & metrics
            "author",
            "reading_time_min",
            "word_count",
            "tags",
            "categories",
            "meta",
            # i18n (flattened)
            "active_locale",
            "available_locales",
            "title",
            "summary",
            "body_html",
            "seo_title",
            "seo_desc",
            # media
            "hero_image_data",
        )


class PublicPageSerializer(BaseTranslatedSerializer):
    class Meta:
        model = Page
        fields = (
            "id",
            "site",
            "slug",
            "is_home",
            "meta",
            # i18n (flattened)
            "active_locale",
            "available_locales",
            "title",
            "body_html",
            "seo_title",
            "seo_desc",
            # media
            "hero_image_data",
        )
