from django.db.models.signals import post_save,pre_save,post_delete

from django.dispatch import receiver
from .models import Payment
from django.core.cache import cache

@receiver([post_save, post_delete], sender=Payment)
def invalidate_member_cache(sender, instance, **kwargs):
    cache.delete("payment_list")
    cache.delete("curd-payment")
  