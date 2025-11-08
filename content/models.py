import uuid
from django.db import models
from django.utils import timezone
from parler.models import TranslatableModel, TranslatedFields
from core.models import TimeStamped, Site, Author, MediaAsset
from taxonomy.models import Tag, Category

class PublishStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SCHED = "scheduled", "Scheduled"
    PUBL  = "published", "Published"
    ARCH  = "archived", "Archived"

class Post(TranslatableModel, TimeStamped):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    site = models.CharField(max_length=16, choices=Site.choices)
    slug = models.SlugField(max_length=160)
    status = models.CharField(max_length=12, choices=PublishStatus.choices, default=PublishStatus.DRAFT)
    published_at = models.DateTimeField(default=timezone.now)
    unlisted = models.BooleanField(default=False)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name="posts")
    hero_image = models.ForeignKey(MediaAsset, null=True, blank=True, on_delete=models.SET_NULL)
    reading_time_min = models.PositiveSmallIntegerField(default=0)
    word_count = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    categories = models.ManyToManyField(Category, blank=True, related_name="posts")
    meta = models.JSONField(default=dict, blank=True)

    translations = TranslatedFields(
        title = models.CharField(max_length=200),
        summary = models.CharField(max_length=350, blank=True),
        body_md = models.TextField(),
        seo_title = models.CharField(max_length=200, blank=True),
        seo_desc  = models.CharField(max_length=160, blank=True),
    )

    class Meta:
        unique_together = [("site","slug")]
        ordering = ["-published_at"]

class Page(TranslatableModel, TimeStamped):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    site = models.CharField(max_length=16, choices=Site.choices)
    slug = models.SlugField(max_length=160)
    is_home = models.BooleanField(default=False)
    hero_image = models.ForeignKey(MediaAsset, null=True, blank=True, on_delete=models.SET_NULL)
    meta = models.JSONField(default=dict, blank=True)

    translations = TranslatedFields(
        title = models.CharField(max_length=200),
        body_md = models.TextField(),
        seo_title = models.CharField(max_length=200, blank=True),
        seo_desc  = models.CharField(max_length=160, blank=True),
    )

    class Meta:
        unique_together = [("site","slug")]
