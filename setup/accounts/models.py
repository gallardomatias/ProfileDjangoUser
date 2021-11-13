from django.db import models
from django.contrib.auth.models import AbstractUser,Group
from django.conf import settings
import os
from django.db.models.base import Model
from django.db.models.signals import post_save

#Extensión del usuario
CHOICES_OPTIONS = (
    ('1', "Administrador"),
    ('2', "Profesional"),
    ('3', "Cliente"),
    ) 

class User(AbstractUser):
    tipo_perf = models.CharField(max_length=1, choices=CHOICES_OPTIONS)
    REQUIRED_FIELDS = ['tipo_perf']

class Profile(models.Model):
    #OneToOneField significara que un perfil tiene un usuario
    #on_delete=models.CASCADE todo lo que pertenece a User se borra/desactiva
    # related_name es el nombre que se utilizará para la relación del objeto relacionado con este.
    # auto_now_add=True se agrega automaticamente la fecha cuando se crea el modelo
    # null=True Si es True, Django almacenará valores vacíos como NULL en la base de datos. El valor predeterminado es falso.
    #blank=True Si es Verdadero, se permite que el campo esté en blanco. El valor predeterminado es falso.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    group = models.ForeignKey(Group,on_delete=models.DO_NOTHING)
    rut = models.CharField(max_length=12, null=True, blank=True)
    telefono = models.CharField(max_length=12, null=True, blank=True)
    direccion = models.CharField(max_length=200,null=True, blank=True)
    fecha_creado = models.DateField(auto_now_add=True)
    
    def __str__(self):
        #En el modelo Profile, siempre se vera el nombre de usuario del modelo User interno de django
        return self.user.username


#Manera de asignar un usuario a un perfil cuando es registrado
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
#created_profile
post_save.connect(create_user_profile, sender=User)
#save_profile
post_save.connect(save_user_profile, sender=User)


##################################################################################################
#extension del perfil de usuario a un cliente y profesional

class Cliente(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE,related_name='client')
    razon_social = models.CharField(max_length=50)

    def __str__(self):
        return self.profile.user.username

class Profesional(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE,related_name='professional')
    def __str__(self):
        return self.profile.user.username


def create_profile_client(sender,instance, created,**kwargs):
    if created: 
        if User.objects.all().filter(tipo_perf='2'):
            Profesional.objects.create(profile=instance)
            instance.professional.save()
        elif User.objects.all().filter(tipo_perf='3'):
            Cliente.objects.create(profile=instance)
            instance.client.save()

#def save_profile_client(sender, instance,**kwargs):
    

post_save.connect(create_profile_client,sender = Profile)
#post_save.connect(save_profile_client,sender = Profile)

##########################################################################


