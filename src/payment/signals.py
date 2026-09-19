from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Payment


@receiver([post_save, post_delete], sender=Payment)
def invalidate_payment_cache(sender, instance, **kwargs):
    cache.delete("payment_list")
    cache.delete(f"payment_detail_{instance.id}")
    cache.delete("dashboard")