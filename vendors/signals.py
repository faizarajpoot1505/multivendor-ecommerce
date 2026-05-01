from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from .models import Vendor

@receiver(post_save, sender=User)
def create_vendor_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'vendor':
        Vendor.objects.create(user=instance, shop_name=instance.username)