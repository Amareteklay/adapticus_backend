from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from content.views import PublicPostViewSet, PublicPageViewSet

router = DefaultRouter()
router.register(r"content/posts", PublicPostViewSet, basename="posts")
router.register(r"content/pages", PublicPageViewSet, basename="pages")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("api/v1/", include(router.urls)),
]
