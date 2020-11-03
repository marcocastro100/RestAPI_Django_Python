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

#Call this file in the views
#create a object with AppletForm with a view
#return this object inside a html <form></form>
#with the form as a context var, in the html form, do: {{form.as_<html tag to exibe>(p,ul,div...)}}
#form.is_valid(): django auto validation of the form