from django import forms
from inmueble.models import Lote

class NuevoLote(forms.ModelForm):
    class Meta:
        model = Lote
        fields = '__all__'
 
