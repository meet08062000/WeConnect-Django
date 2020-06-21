from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Post


@receiver(pre_delete, sender=Post)
def post_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
