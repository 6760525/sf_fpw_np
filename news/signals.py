from django.shortcuts import redirect
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Post, Category
#from .tasks import email_notification
from django.urls import reverse_lazy

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        #for u in subs:
            #email_notification.apply_async([instance.id, created, u], countdown=5)
        pass