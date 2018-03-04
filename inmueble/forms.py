from django import forms
from inmueble.models import Lote, TipoInmueble
from proyecto.models import Etapa
from django.forms import BaseInlineFormSet, inlineformset_factory
from django.utils.translation import ugettext_lazy as _



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


class TipoInmuebleForm(forms.ModelForm):
    """Form definition for Inventario."""

    class Meta:
        """Meta definition for Inventarioform."""

        model = TipoInmueble
        exclude = (
                'etapa',
                )

        labels = {
            'nombreTipoInmueble': _('Nombre Inmuebles'),
            'areaTipoInmueble': _('Área de Inmuebles (M2)'),
            'noUnidadesTipoInmueble': _('# Unidades a Vender'),
            'valorM2TipoInmueble': _('Valor por M2'),
            'secundarioTipoInmueble': _('¿Es inmueble secundario?'),
            'paramInmueble': _('Clase de Inmueble'),
            'valorSalariosMinTipoInmueble': _('Valor en Salarios Mínimos'),
        }


InventarioFormSet = inlineformset_factory(Etapa, TipoInmueble, form=TipoInmuebleForm, extra=1, can_delete=True)