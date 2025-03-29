from django import forms
from .models import enquete, questions, responseSelection, enqueteResponse, reponses


class enqueteForm(forms.ModelForm):
    class Meta:
        model = enquete
        fields = ['code', 'name', 'description', 'end_date']
        widgets = {
            'code' : forms.TextInput(attrs={'class' : ''}),
            'name' : forms.TextInput(attrs={'class' : ''}),
            'descriptiom' : forms.TextInput(attrs={'class' : ''}),
            'end_date' : forms.DateInput(attrs={'class' : '', 'type' : 'date'}),
        }