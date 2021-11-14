from rest_framework import serializers
from accounts import models

class HelloSerializer(serializers.Serializer):
    """Serializar un campo para probar nuestro APIView"""
    name = serializers.CharField(max_length=10)

class UserSerializer(serializers.ModelSerializer):
    """ Serializa objeto de User"""
    class Meta:
        model = models.User
        fields = ('id', 'username','tipo_perf','password')
        extra_kwargs = {
            'password':{
                'write_only':True,
                'style': {'input_type':'password'}
            }
        }
    
        