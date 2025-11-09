# core/views.py
from __future__ import annotations

from typing import Optional
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response

from .models import NavigationMenu, Setting
from .serializers import NavigationMenuSerializer, SiteSettingsSerializer
from content.utils import request_site


SITE_PARAM = OpenApiParameter(
    name="site",
    location=OpenApiParameter.QUERY,
    required=True,
    description="Site key: amare | adapticus",
    type=str,
)

SLUG_PARAM = OpenApiParameter(
    name="slug",
    location=OpenApiParameter.QUERY,
    required=False,
    description="Menu slug (e.g., 'main', 'footer'). If omitted, returns all menus for the site.",
    type=str,
)


@extend_schema(parameters=[SITE_PARAM, SLUG_PARAM])
class NavigationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = NavigationMenuSerializer

    def get_queryset(self):
        qs = NavigationMenu.objects.all()
        site = request_site(self.request)
        if not site:
            return NavigationMenu.objects.none()
        slug: Optional[str] = self.request.query_params.get("slug")
        qs = qs.filter(site=site)
        if slug:
            qs = qs.filter(slug=slug)
        return qs

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset().order_by("slug").prefetch_related("items")
        menus = list(qs)
        for m in menus:
            items = list(m.items.all().order_by("order", "created_at", "id"))
            setattr(m, "_prefetched_items", items)
        ser = self.get_serializer(menus, many=True)
        return Response(ser.data)


@extend_schema(parameters=[SITE_PARAM])
class SettingsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    GET /api/v1/settings/?site=amare
    returns:
    {
      "site": "amare",
      "settings": { "<key>": <json>, ... }
    }
    """
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        site = request_site(request)
        if not site:
            return Response({"detail": "Missing or invalid ?site parameter."}, status=400)
        qs = Setting.objects.filter(site=site)
        ser = SiteSettingsSerializer.from_queryset(site, qs)
        return Response(ser.data)
