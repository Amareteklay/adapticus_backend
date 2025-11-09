from django.contrib import admin
from .models import Setting, MediaAsset, Author, NavigationMenu, NavigationItem

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ("site", "key", "updated_at")
    list_filter = ("site",)
    search_fields = ("key",)
    ordering = ("site", "key")


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ("id", "kind", "file", "width", "height", "duration_ms", "alt_text")
    list_filter = ("kind",)
    search_fields = ("file", "alt_text", "caption", "checksum")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "site", "url")
    list_filter = ("site",)
    search_fields = ("name", "slug")
    autocomplete_fields = ("avatar",)
    readonly_fields = ("created_at", "updated_at")


class NavigationItemInline(admin.TabularInline):
    model = NavigationItem
    fk_name = "menu"
    extra = 1
    fields = ("label", "url", "order", "parent", "new_tab", "is_active")
    ordering = ("order",)
    show_change_link = True


@admin.register(NavigationMenu)
class NavigationMenuAdmin(admin.ModelAdmin):
    list_display = ("site", "slug")
    list_filter = ("site",)
    search_fields = ("slug",)
    inlines = [NavigationItemInline]


@admin.register(NavigationItem)
class NavigationItemAdmin(admin.ModelAdmin):
    list_display = ("label", "menu", "order", "parent", "new_tab")
    list_filter = ("menu__site", "menu__slug", "new_tab")
    search_fields = ("label", "url")
    ordering = ("menu__slug", "order")
