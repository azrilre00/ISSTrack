from .models import TimeISS
from django import forms
from django.forms import ModelForm, widgets


class ISSForm(forms.ModelForm):
    class Meta:
        model = TimeISS
        fields = ('datetimes',)
        widgets = {
            'datetimes':forms.DateTimeInput(format=('%d/%m/%Y %H:%M:%S'),
                attrs={'type': 'datetime'}),
        }

