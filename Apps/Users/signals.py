from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from Apps.Users.models import User, Autor


@receiver(post_save, sender=get_user_model())
def create_user_autor(sender, instance, created, **kwargs):
    if created:
        print(instance)
        Autor.objects.create(user=instance)
