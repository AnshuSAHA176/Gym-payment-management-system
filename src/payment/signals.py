from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import Payment


@receiver([post_save, post_delete], sender=Payment)
def invalidate_payment_cache(sender, instance, **kwargs):

    cache.delete("dashboard")

    version = cache.get(
        "payment_cache_version",
        1,
    )

    cache.set(
        "payment_cache_version",
        version + 1,
        timeout=None,
    )