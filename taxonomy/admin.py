from django.contrib import admin
from .models import Tag, Category

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("site","name","slug","is_active")
    list_filter = ("site",)
    search_fields = ("name","slug")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("site","name","slug","parent","is_active")
    list_filter = ("site",)
    search_fields = ("name","slug")
