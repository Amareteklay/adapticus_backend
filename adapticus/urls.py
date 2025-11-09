# adapticus/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from content.views import PublicPostViewSet, PublicPageViewSet
from core.views import NavigationViewSet, SettingsViewSet

router = DefaultRouter()
router.register(r"content/posts", PublicPostViewSet, basename="posts")
router.register(r"content/pages", PublicPageViewSet, basename="pages")
router.register(r"navigation", NavigationViewSet, basename="navigation")
router.register(r"settings", SettingsViewSet, basename="settings")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("api/v1/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
