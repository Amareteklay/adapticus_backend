# core/serializers.py
from __future__ import annotations

from typing import Dict, List
from rest_framework import serializers
from .models import NavigationMenu, NavigationItem, Setting


# ---------- Navigation ----------

class NavigationItemNodeSerializer(serializers.Serializer):
    label = serializers.CharField()
    url = serializers.CharField()
    new_tab = serializers.BooleanField()
    order = serializers.IntegerField()
    children = serializers.ListField(child=serializers.DictField(), source="children_list")


class NavigationMenuSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = NavigationMenu
        fields = ("id", "site", "slug", "items")

    def get_items(self, obj: NavigationMenu):
        items = list(getattr(obj, "_prefetched_items", None) or obj.items.all())
        children_map: Dict[str | None, List[NavigationItem]] = {}
        for it in items:
            children_map.setdefault(it.parent_id, []).append(it)
        for siblings in children_map.values():
            siblings.sort(key=lambda x: (x.order, x.label.lower()))

        def build(node: NavigationItem) -> dict:
            kids = children_map.get(node.id, [])
            return {
                "label": node.label,
                "url": node.url,
                "new_tab": node.new_tab,
                "order": node.order,
                "children_list": [build(k) for k in kids],
            }

        roots = children_map.get(None, [])
        return [build(r) for r in roots]


# ---------- Settings ----------

class SiteSettingsSerializer(serializers.Serializer):
    """
    Simple wrapper that returns all settings for a site as a single dict.
    Example:
    {
      "site": "amare",
      "settings": {
        "site_title": "Amare Teklay",
        "social_links": [{"label":"GitHub","href":"..."}],
        "footer_html": "<p>...</p>",
        "seo_defaults": {"title_suffix":" · Amare Teklay"}
      }
    }
    """
    site = serializers.CharField()
    settings = serializers.DictField(child=serializers.JSONField())

    @staticmethod
    def from_queryset(site: str, qs):
        data = {row.key: row.value for row in qs}
        # Optional: normalize some common keys with safe defaults
        data.setdefault("site_title", "Amare Teklay")
        data.setdefault("social_links", [])
        data.setdefault("footer_html", "")
        data.setdefault("seo_defaults", {})
        return SiteSettingsSerializer({"site": site, "settings": data})
