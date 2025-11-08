import uuid
from django.db import models

class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active  = models.BooleanField(default=True)
    class Meta:
        abstract = True

class Site(models.TextChoices):
    AMARE = "amare", "Amare Teklay"
    ADAPT = "adapticus", "Homo Adapticus"

class MediaAsset(TimeStamped):
    KIND_CHOICES = [("image","Image"),("document","Document"),("audio","Audio"),("video","Video"),("other","Other")]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kind = models.CharField(max_length=12, choices=KIND_CHOICES, default="image")
    file = models.FileField(upload_to="media/")
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    duration_ms = models.PositiveIntegerField(null=True, blank=True)
    checksum = models.CharField(max_length=64, blank=True, default="")
    # simple i18n text kept here (Parler not needed for alt/caption, but ok to add later if you prefer)
    alt_text = models.CharField(max_length=200, blank=True, default="")
    caption  = models.CharField(max_length=300, blank=True, default="")
    meta = models.JSONField(default=dict, blank=True)

class Author(TimeStamped):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True)
    bio  = models.TextField(blank=True)
    url  = models.URLField(blank=True)
    avatar = models.ForeignKey(MediaAsset, null=True, blank=True, on_delete=models.SET_NULL)
    # site null = global author usable on both
    site = models.CharField(max_length=16, choices=Site.choices, null=True, blank=True)

class NavigationMenu(TimeStamped):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    site = models.CharField(max_length=16, choices=Site.choices)
    slug = models.SlugField(max_length=80) # e.g., main, footer
    class Meta:
        unique_together = [("site","slug")]

class NavigationItem(TimeStamped):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu = models.ForeignKey(NavigationMenu, on_delete=models.CASCADE, related_name="items")
    label = models.CharField(max_length=120)
    url = models.CharField(max_length=300)
    order = models.PositiveIntegerField(default=0)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    new_tab = models.BooleanField(default=False)

class Redirect(TimeStamped):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    site = models.CharField(max_length=16, choices=Site.choices)
    source_path = models.CharField(max_length=300)  # like /old-about
    target_url = models.CharField(max_length=500)
    http_status = models.PositiveSmallIntegerField(default=301)
    class Meta:
        unique_together = [("site","source_path")]

class Setting(TimeStamped):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    site = models.CharField(max_length=16, choices=Site.choices)
    key  = models.SlugField(max_length=80)
    value = models.JSONField(default=dict, blank=True)
    class Meta:
        unique_together = [("site","key")]
