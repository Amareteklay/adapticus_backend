# content/views.py
from __future__ import annotations

from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Post, Page, PublishStatus
from .serializers import PublicPostSerializer, PublicPageSerializer
from .utils import request_lang, request_site


LANG_PARAM = OpenApiParameter(
    name="lang",
    location=OpenApiParameter.QUERY,
    required=False,
    description="Language code: en, sv, ti-et. Falls back to Accept-Language or 'en'.",
    type=str,
)

SITE_PARAM = OpenApiParameter(
    name="site",
    location=OpenApiParameter.QUERY,
    required=False,
    description="Filter by site: amare | adapticus.",
    type=str,
)


@extend_schema(parameters=[LANG_PARAM, SITE_PARAM])
class PublicPostViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    GET /api/v1/content/posts/?site=amare&lang=sv     (paginated list)
    GET /api/v1/content/posts/<slug>/?site=amare&lang=sv
    """
    serializer_class = PublicPostSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        qs = (
            Post.objects.filter(status=PublishStatus.PUBL, unlisted=False)
            .select_related("author", "hero_image", "author__avatar")
            .prefetch_related("tags", "categories")
            .order_by("-published_at")
        )
        site = request_site(self.request)
        return qs.filter(site=site) if site else qs

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["lang"] = request_lang(self.request)
        return ctx


@extend_schema(parameters=[LANG_PARAM, SITE_PARAM])
class PublicPageViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    GET /api/v1/content/pages/?site=amare&lang=sv      (paginated list)
    GET /api/v1/content/pages/<slug>/?site=amare&lang=sv
    """
    serializer_class = PublicPageSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        qs = Page.objects.select_related("hero_image").order_by("slug")
        site = request_site(self.request)
        return qs.filter(site=site) if site else qs

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["lang"] = request_lang(self.request)
        return ctx
