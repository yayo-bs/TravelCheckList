from django import forms
from .models import Trip


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip  # Modelo sobre el que se basa el formulario

        # Campos que queremos mostrar al usuario
        fields = ['title', 'destination', 'start_date', 'end_date', 'notes']

        # Widgets para mejorar la visualización del formulario
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }