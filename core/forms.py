from django import forms
from .models import Abono

class AbonoForm(forms.ModelForm):
    class Meta:
        model = Abono
        fields = ['monto_abonado']
        widgets = {
            'monto_abonado': forms.NumberInput(attrs={'step': '0.01'})
        }
        