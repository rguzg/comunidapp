from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from Apps.Users.models import Tesis, User, Autor, UpdateRequest, Articulo, CapituloLibro, Patente, Congreso, Investigacion
from .AñadirRelacion import AñadirRelacion
from typing import Union

# Señal que crea un Autor de manera automatica cada vez que es creado un nuevo usuario
@receiver(post_save, sender=get_user_model())
def create_user_autor(sender, instance, created, **kwargs):
    if created:
        Autor.objects.create(user=instance)
        UpdateRequest.objects.create(
            user=instance,
            estado='A'
        )

# Señal que crea las relaciones de un producto de manera automática cada vez que se crea un producto
@receiver(post_save, sender = Articulo)
@receiver(post_save, sender = CapituloLibro)
@receiver(post_save, sender = Patente)
@receiver(post_save, sender = Congreso)
@receiver(post_save, sender = Investigacion)
@receiver(post_save, sender = Tesis)
def crear_relaciones(sender: Union[Articulo, CapituloLibro, Patente, Congreso, Investigacion, Tesis], instance: Union[Articulo, CapituloLibro, Patente, Congreso, Investigacion, Tesis], created: bool, **kwargs):
    if created:
        AñadirRelacion(instance)
