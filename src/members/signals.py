from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import Member


@receiver([post_save, post_delete], sender=Member)
def invalidate_member_cache(sender, instance, **kwargs):

    cache.delete("dashboard")

    version = cache.get(
        "member_cache_version",
        1,
    )

    cache.set(
        "member_cache_version",
        version + 1,
        timeout=None,
    )