from django.contrib import admin
from .models import Author, MediaAsset, NavigationMenu, NavigationItem, Redirect, Setting

admin.site.register(Author)
admin.site.register(MediaAsset)
admin.site.register(NavigationMenu)
admin.site.register(NavigationItem)
admin.site.register(Redirect)
admin.site.register(Setting)
