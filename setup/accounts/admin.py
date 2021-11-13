from django.contrib import admin

from .models import Profile,Cliente,Profesional,User
# Register your models here.


admin.site.register(Profile)
admin.site.register(Cliente)
admin.site.register(Profesional)
admin.site.register(User)