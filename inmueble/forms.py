from django import forms
from inmueble.models import Lote, TipoInmueble
from proyecto.models import SubEtapa
from django.forms import BaseInlineFormSet, inlineformset_factory, modelformset_factory
from django.utils.translation import ugettext_lazy as _



class CrearLoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = '__all__'
        exclude = ('valorTotalLote','mesesDePagoLote','nombreLote','areaBrutaLote')

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
        labels = {
            'areaCesionViasLote': _('Área de Cesión en Vías (M2)'),
            'porcentajeCesionVerdesLote': _('% Cesión áreas verdes'),
            'areaCesionTierraLote': _('Área de Cesión (M2)'),
            'valorM2Cesion': _('Valor del M2 en Cesión'),
            'valorLote': _('Valor del Lote'),
            'valorPorcentajeLote': _('% del Valor del Lote sobre proyecto'),
            'valorEnPorcentaje': _('¿Cargar valor del Lote al proyecto?'),
            'porcentajeFinanciarLote': _('% de financiación del lote'),
            'mesesGraciaInteresesLote': _('# de meses de gracia en el pago del lote'),
            'tasaInteresMensualLote': _('% tasa de interés del lote'),
            'mesesTotalesPagoLote': _('Plazo de pago en meses'),
        }


class TipoInmuebleForm(forms.ModelForm):
    """Form definition for Inventario."""

    class Meta:
        """Meta definition for Inventarioform."""

        model = TipoInmueble
        exclude = (
                'subEtapa',
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


class TipoInmuebleAutoForm(forms.ModelForm):
    """Form definition for Inventario."""

    class Meta:
        """Meta definition for Inventarioform."""

        model = TipoInmueble
        fields = '__all__'

        labels = {
            'nombreTipoInmueble': _('Nombre Inmuebles'),
            'areaTipoInmueble': _('Área de Inmuebles (M2)'),
            'noUnidadesTipoInmueble': _('# Unidades a Vender'),
            'valorM2TipoInmueble': _('Valor por M2'),
            'secundarioTipoInmueble': _('¿Es inmueble secundario?'),
            'paramInmueble': _('Clase de Inmueble'),
            'valorSalariosMinTipoInmueble': _('Valor en Salarios Mínimos'),
        }

InventarioFormSet = inlineformset_factory(SubEtapa, TipoInmueble, form=TipoInmuebleForm, extra=1, can_delete=True)