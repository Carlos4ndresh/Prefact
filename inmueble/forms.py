from django import forms
from inmueble.models import Lote

class CrearLoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = '__all__'
        exclude = ('valorTotalLote','mesesDePagoLote')

        widgets = {
            'areaBrutaLote' : forms.NumberInput(),
            'areaCesionViasLote' : forms.NumberInput(),
            'porcentajeCesionVerdesLote' : forms.NumberInput(),
            'areaCesionTierraLote' : forms.NumberInput(),
            'valorM2Cesion' : forms.NumberInput(),
            'valorLote' : forms.NumberInput(),
            'valorPorcentajeLote' : forms.NumberInput(),
            'valorEnPorcentaje' : forms.CheckboxInput(),
            'porcentajeFinanciarLote' : forms.NumberInput(),
            'tasaInteresMensualLote' : forms.NumberInput(),
            'mesesTotalesPagoLote' : forms.NumberInput(),
        }

