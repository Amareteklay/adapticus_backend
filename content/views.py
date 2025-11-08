from rest_framework import viewsets, permissions, filters
from .models import Post, Page
from .serializers import PostSerializer, PageSerializer

class PublicPostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Post.objects.filter(status="published").select_related("author","hero_image").prefetch_related("tags","categories")
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["translations__title","translations__summary","translations__body_md","slug"]
    ordering_fields = ["published_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        site = self.request.query_params.get("site")
        lang = self.request.query_params.get("lang")
        tag = self.request.query_params.get("tag")
        if site: qs = qs.filter(site=site)
        if tag: qs = qs.filter(tags__slug=tag)
        if lang: qs = qs.active_translations(language_code=lang)
        return qs

class PublicPageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PageSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Page.objects.all().select_related("hero_image")
    lookup_field = "slug"

    def get_queryset(self):
        qs = super().get_queryset()
        site = self.request.query_params.get("site")
        lang = self.request.query_params.get("lang")
        if site: qs = qs.filter(site=site)
        if lang: qs = qs.active_translations(language_code=lang)
        return qs
