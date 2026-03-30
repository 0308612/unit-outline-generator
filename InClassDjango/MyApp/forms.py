from django import forms

from .models import teacher



class InputForm(forms.ModelForm):
    
    class Meta:

        model = teacher

        fields = ['Name', 'Area', 'VET', 'PDF_Title', 'PDF_File']