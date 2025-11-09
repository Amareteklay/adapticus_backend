import os, json, requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Page, PublishStatus

REVALIDATE_URL = os.environ.get("REVALIDATE_URL")
REVALIDATE_SECRET = os.environ.get("REVALIDATE_SECRET")

def _notify(payload: dict):
    if not (REVALIDATE_URL and REVALIDATE_SECRET):
        return
    try:
        requests.post(
            REVALIDATE_URL,
            params={"secret": REVALIDATE_SECRET},
            json=payload,
            timeout=4.0,
        )
    except Exception:
        # keep failures silent; site will still update on ISR timers
        pass

@receiver(post_save, sender=Post)
def revalidate_on_post_save(sender, instance: Post, **kwargs):
    # only ping for published, public posts
    if instance.status == PublishStatus.PUBL and not instance.unlisted:
        _notify({"type": "post", "site": instance.site, "slug": instance.slug})

@receiver(post_save, sender=Page)
def revalidate_on_page_save(sender, instance: Page, **kwargs):
    _notify({"type": "page", "site": instance.site, "slug": instance.slug})
