from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os
from django.db.models.base import Model
from django.db.models.signals import post_save

#Extensión del usuario
class Profile(models.Model):
    #OneToOneField significara que un perfil tiene un usuario
    #on_delete=models.CASCADE todo lo que pertenece a User se borra/desactiva
    # related_name es el nombre que se utilizará para la relación del objeto relacionado con este.
    # auto_now_add=True se agrega automaticamente la fecha cuando se crea el modelo
    # null=True Si es True, Django almacenará valores vacíos como NULL en la base de datos. El valor predeterminado es falso.
    #blank=True Si es Verdadero, se permite que el campo esté en blanco. El valor predeterminado es falso.

    CHOICES_OPTIONS = (
    ('1', "Administrador"),
    ('2', "Profesional"),
    ('3', "Cliente"),
    ) 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    rut = models.CharField(max_length=12, null=True, blank=True)
    telefono = models.CharField(max_length=12, null=True, blank=True)
    direccion = models.CharField(max_length=200,null=True, blank=True)
    tipo_perf = models.CharField(max_length=1, choices=CHOICES_OPTIONS)
    fecha_creado = models.DateField(auto_now_add=True)
    
    def __str__(self):
        #En el modelo Profile, siempre se vera el nombre de usuario del modelo User interno de django
        return self.user.username


#Manera de asignar un perfil a un usuario cuando es registrado
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
#created_profile
post_save.connect(create_user_profile, sender=User)
#save_profile
post_save.connect(save_user_profile, sender=User)

