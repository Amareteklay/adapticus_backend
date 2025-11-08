from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField
from .models import Post, Page

class PostSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Post)
    class Meta:
        model = Post
        fields = ["id","site","slug","status","published_at","unlisted",
                  "author","hero_image","reading_time_min","word_count",
                  "tags","categories","meta","translations"]

class PageSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Page)
    class Meta:
        model = Page
        fields = ["id","site","slug","is_home","hero_image","meta","translations"]
