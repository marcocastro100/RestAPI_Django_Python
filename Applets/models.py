from django.db import models

INTERATIONTYPES = [(1,'Animação'),(1,'Rolagem de barra'),(1,'Inserir número')]
AREAS = [(1,'Geometria',),(2,'Cálculo'),(3,'Estatística'),(4,'Aritimética'),(5,'Trigonometria'),(6,'Álgebra'),(7,'Probabilidade'),(8,'Funções')]
LANGUAGES = [(1,'Português'),(2,'Ingles')]

class Applet(models.Model):
    #General
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 100)
    language = models.IntegerField(choices=LANGUAGES)
    #Technical
    location = models.CharField(max_length = 100,default='Url') #URL
    #Educational
    InteractivityType = models.IntegerField(choices=INTERATIONTYPES)
    context = models.IntegerField(choices=AREAS)
    #Rights
    copyright = models.CharField(max_length = 50,default='Autor') #nome do autor do applet