from django import forms 
from proyecto.models import (Proyecto, Macroproyecto, Venta, Etapa, 
                            SubEtapa, ProyeccionIPC, TablaIPC)
from django.forms import BaseInlineFormSet, inlineformset_factory
                            

class MacroproyectoForm(forms.ModelForm):
    """Form definition for Macroproyecto."""

    class Meta:
        """Meta definition for Macroproyectoform."""

        model = Macroproyecto
        fields = ('nombreMacroproyecto','descripcionMacroproyecto','m2Macroproyecto')

        widgets = {
            'nombreMacroproyecto' : forms.TextInput(),
            'descripcionMacroproyecto' : forms.Textarea(),
            'm2Macroproyecto' : forms.NumberInput
        }


class ProyectoForm(forms.ModelForm):
    """Form definition for Proyecto."""

    class Meta:
        """Meta definition for Proyectoform."""

        model = Proyecto
        # fields = ('',)
        # fields = '__all__'
        exclude = ('macroproyecto',)
    

ProyectoFormSet = inlineformset_factory(Macroproyecto,Proyecto,form=ProyectoForm, extra=5,exclude=('macroproyecto',), labels={
            'nombreProyecto': ("Nombre"),
            'descripcionProyecto': ("Descripción"),
            'm2PorProyecto': ("Metros Cuadrados"),
            }, can_delete=True)

class VentaForm(forms.ModelForm):
    """Form definition for Venta."""

    class Meta:
        """Meta definition for Ventaform."""

        model = Venta
        # fields = ('',)
        fields = '__all__'
        exclude = (
            'volumenTotalVenta',
            'proyecto',
            'volumenInicialesVenta',
            'reajusteVenta'
            )

VentaFormSet = inlineformset_factory(Proyecto, Venta, form=VentaForm, 
            exclude=(
                'proyecto',
                'volumenTotalVenta',
                'volumenInicialesVenta',
                'reajusteVenta',
                ), 
            labels={
                'velocidadVentas': ("Velocidad"),
                'porcentajeTopeRemanenteVentas': ("%Tope Remanente"),
                'velocidadUltimasVentas': ("Vel. Ult. Ventas"),
                'porcentajeTopeInicialVentas': ("%Tope Inicial"),
                'porcentajeVelocidadInicialVentas': ("%Velocidad Inicial"),
                'fechaInicioVentas': ("Fecha Inicio"),
                'numeroDeIncrementos': ("#Incrementos"),
                'porcenReajusteIncremento': ("%Reajuste Incr."),
                'tipoIncremento': ("Tipo Incr."),
                'porcenTopeReajusteIncremento': ("%Tope Reajuste"),
            },
            can_delete=False)

class EtapaForm(forms.ModelForm):
    """Form definition for Etapa."""

    class Meta:
        """Meta definition for Etapaform."""

        model = Etapa
        # fields = ('',)
        fields = '__all__'

class SubEtapaForm(forms.ModelForm):
    """Form definition for SubEtapa."""

    class Meta:
        """Meta definition for SubEtapaform."""

        model = SubEtapa
        # fields = ('',)
        fields = '__all__'

''' class IncrementoForm(forms.ModelForm):
    """Form definition for Incremento."""

    class Meta:
        """Meta definition for Incrementoform."""

        model = Incremento
        # fields = ('',)
        fields = '__all__'
 '''
class ProyeccionIPCForm(forms.ModelForm):
    """Form definition for ProyeccionIPC."""

    class Meta:
        """Meta definition for ProyeccionIPCform."""

        model = ProyeccionIPC
        # fields = ('',)
        fields = '__all__'


class TablaIPCForm(forms.ModelForm):
    """Form definition for TablaIPC."""

    class Meta:
        """Meta definition for TablaIPCform."""

        model = TablaIPC
        # fields = ('',)
        fields = '__all__'









