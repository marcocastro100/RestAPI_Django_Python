from django.db import models

INTERATIONTYPES = [('Animacao','Animação'),('BarRolling','BarRolling'),('Number','Inserir número')]
AREAS = [('Geometria','Geometria',),('Calculo','Cálculo'),('Estatistica','Estatística'),
('Aritimetica','Aritimética'),('Trigonometria','Trigonometria'),('Algebra','Álgebra'),
('Probabilidade','Probabilidade'),('Funcoes','Funções')]
LANGUAGES = [('PT','Português'),('EN','Ingles')]

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
