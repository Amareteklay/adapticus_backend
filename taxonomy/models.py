import uuid
from django.db import models
from core.models import TimeStamped, Site

class Tag(TimeStamped):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    site = models.CharField(max_length=16, choices=Site.choices)
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=80)
    description = models.CharField(max_length=200, blank=True, default="")
    class Meta:
        unique_together = [("site","slug")]

class Category(TimeStamped):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    site = models.CharField(max_length=16, choices=Site.choices)
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=80)
    description = models.CharField(max_length=200, blank=True, default="")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    class Meta:
        unique_together = [("site","slug")]
