from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .documents import ProductDocument
from .models import Product


@receiver(post_save, sender=Product)
def update_document(sender, instance, **kwargs):
    ProductDocument().update(instance)

@receiver(post_delete, sender=Product)
def delete_document(sender, instance, **kwargs):
    ProductDocument().delete(instance)
