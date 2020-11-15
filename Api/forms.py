from django import forms #work with forms
from .models import Applet #my model

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
class SearchForm(forms.ModelForm):
    class Meta:
        model = Applet;
        fields = ['language','context']