from django.db.models import query
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.contrib.auth.models import User
from rest_framework.decorators import authentication_classes, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from .models import Profile

#Django Rest Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
#Django Rest Framework Login
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

# Api viewsets
from rest_framework import viewsets

#import Serializers
from accounts import serializers, models

def main(request):
    return render(request, 'accounts/main.html', {})

class UserProfileView(View):
    def get(self,request,username,*args,**kwargs):
        user = get_object_or_404(User, username=username)
        profile = Profile.objects.get(user=user)
        context={
            'user':user,
            'profile':profile
        }
        return render(request,'accounts/main.html',context)


# A P I View

class HelloApiView(APIView):
    """ API View de prueba"""
    serializer_class = serializers.HelloSerializer

    def get(self, request,format=None):
        """ Retornar lista de caracteristicas del APIView"""
        an_apiview =[
            'Usamos metodos HTTP como funciones (get,post,patch,put,delete)',
            'Es similar a una vista tradicional de Django',
            'Nos da el mayor control sobre la logica de nuestra aplicacion',
            'Esta mapeado manualmente a los URLs'
        ]
        return Response({'message':'Hello','an_apiview':an_apiview})
    
    def post(self, request):
        """ Crea un mensaje con nuestro nombre"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def put(self,request,pk=None):
        """Maneja actualizar un objeto"""
        return Response({'method': 'PUT'})
    
    def patch(self, request,pk=None):
        """Maneja actualizacion parcial de un objecto"""
        return Response({'method':'PATCH'})

    def delete(self, request,pk=None):
        """Borrar un objeto"""
        return Response({'method':' DELETE'})
    
#A P I ViewSet

class HelloViewSet(viewsets.ViewSet):

    """ Test API ViewSet """
    serializer_class = serializers.HelloSerializer
    def list(self, request):
        """Retorna un mensaj de Hola mundo"""
        a_viewset = [
            'Usa acciones (list,create,retrieve,update,partial_update)',
            'Automaticamente mapea a los URLs usando Routers',
            'Provee mas funcionalidad con menos codigo',
        ]
        return Response({'message':'Hola!','a_viewset': a_viewset})
    
    def create(self,request):
        """ Crear nuevo mensaje de hola mundo"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f"Hello {name}"
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self,request,pk=None):
        """obtiene un objeto y su ID"""
        return Response({'http_method': 'GET'})

    def update(self,request,pk=None):
        """Actualiza un objeto"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request,pk=None):
        """Actualizate parcialmente el objeto"""
        return Response({'http_method':'PATCH'})

    def destroy(self, request,pk=None):
        """destruye un objeto"""
        return Response({'http_method':' DELETE'})

class UserViewSet(viewsets.ModelViewSet):
    serializer_class= serializers.UserSerializer
    queryset = models.User.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class UserLoginApiView(ObtainAuthToken):
    """Crea Tokens de autenticacion de usuario"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES