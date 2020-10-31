from rest_framework import serializers #import a serializer
from .models import Applet #import models in this app

class AppletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applet #define o modelo a ser serializado
        fields = '__all__' #todos os atributos devem ser serializados (inclusive id oculto)
        
