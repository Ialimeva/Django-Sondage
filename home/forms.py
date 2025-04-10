from django import forms
from .models import enquete, questions, responseSelection, enqueteResponse, reponses

# Add Enquete form
class enqueteForm(forms.ModelForm):
    class Meta:
        model = enquete
        fields = ['code', 'name', 'description', 'start_date', 'end_date']
        widgets = {
            'code' : forms.TextInput(attrs={'class' : ''}),
            'name' : forms.TextInput(attrs={'class' : ''}),
            'descriptiom' : forms.TextInput(attrs={'class' : ''}),
            'start_date' : forms.DateInput(attrs={'class' : '', 'type' : 'date'}),
            'end_date' : forms.DateInput(attrs={'class' : '', 'type' : 'date'}),
        }
        
# Add Question form
class questionForm(forms.ModelForm):
    class Meta:
        model = questions
        fields = ['question', 'description', 'response_type']
        widgets = {
            'question' : forms.TextInput(attrs={'class' :''}),
            'description' : forms.TextInput(attrs={'class' :''}),
            'response_type' : forms.TextInput(attrs={'class' :''}),
        }

# Add Response Form
class responseForm(forms.ModelForm):
    class Meta:
        model = responseSelection
        fields = ['reponse', 'note']
        widgets = {
            'response' : forms.TextInput(attrs = {'class': ''}),
            'note' : forms.TextInput(attrs = {'class': ''}),
        }