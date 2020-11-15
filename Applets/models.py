INTERATIONTYPES = [('Animacao','Animação'),('BarRolling','BarRolling'),('Number','Inserir número')]
AREAS = [('Geometria','Geometria',),('Calculo','Cálculo'),('Estatistica','Estatística'),
('Aritimetica','Aritimética'),('Trigonometria','Trigonometria'),('Algebra','Álgebra'),
('Probabilidade','Probabilidade'),('Funcoes','Funções')]
LANGUAGES = [('PT','Português'),('EN','Ingles')]

######################________Models.py__________#################################################
from django.db import models
class Applet(models.Model):
    #General
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 100,default='1')
    language = models.CharField(choices=LANGUAGES,default='PT',max_length=20)
    #Technical
    location = models.CharField(max_length = 100,default='Url') #URL
    #Educational
    interactivity = models.CharField(choices=INTERATIONTYPES,default='1',max_length=20)
    context = models.CharField(choices=AREAS,default='1',max_length=20)
    #Rights
    copyright = models.CharField(max_length = 50,default='Autor') #nome do autor do applet

######################________Forms.py__________######################################################
from django import forms #work with forms
class AppletForm(forms.ModelForm):
    class Meta:
        model = Applet; #my model
        fields = [ #fields of my model that will have a form
            'title',
            'description',
            'language',
            'location',
            'interactivity',
            'context',
            'copyright'
        ]
class SearchForm(forms.ModelForm): #Fields used to make a search
    class Meta:
        model = Applet;
        fields = ['language','context']

######################________Serializers.py__________##############################################
from rest_framework import serializers #import a serializer
class AppletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applet #define o modelo a ser serializado
        fields = '__all__' #todos os atributos devem ser serializados (inclusive id oculto)