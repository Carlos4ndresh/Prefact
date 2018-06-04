from django import forms 
from proyecto.models import (Proyecto, Macroproyecto, Venta, Etapa, 
                            SubEtapa, ProyeccionIPC, TablaIPC)
from django.forms import BaseInlineFormSet, inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
                            

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

        labels = {
            'nombreMacroproyecto': _('Nombre del Macroproyecto'),
            'descripcionMacroproyecto': _('Descripción del Macroproyecto'),
            'velocidadUltimasVentas': _('Velocidad (Tasa) de Últimas Ventas'),
            'm2Macroproyecto': _('Área Bruta (M2)'),            
        }

# Form para auto macroproyecto

class MacroEtapaAutoForm(forms.Form):
    numeroProyectos = forms.IntegerField(label="# Proyectos")
    numeroEtapas = forms.IntegerField(label="# Etapas")
    numeroSubEtapas = forms.IntegerField(label="# SubEtapas")

    def clean_numeroProyectos(self):
        dato = self.cleaned_data['numeroProyectos']
        if dato > 3:
            raise ValidationError(_('Número de proyectos inválido, máximo permitido es 3'),code='invalid',params={'Valor':'3'})
        return dato
    
    def clean_numeroEtapas(self):
        dato = self.cleaned_data['numeroEtapas']
        if dato > 3:
            raise ValidationError(_('Número de etapas inválido, máximo permitido es 3'),code='invalid',params={'Valor':'3'})
        return dato
    
    def clean_numeroSubEtapas(self):
        dato = self.cleaned_data['numeroSubEtapas']
        if dato > 3:
            raise ValidationError(_('Número de SubEtapas inválido, máximo permitido es 3'),code='invalid',params={'Valor':'3'})
        return dato
    

class ProyectoForm(forms.ModelForm):
    """Form definition for Proyecto."""

    class Meta:
        """Meta definition for Proyectoform."""

        model = Proyecto
        # fields = ('',)
        # fields = '__all__'
        exclude = ('macroproyecto',)
        labels={
            'nombreProyecto': ("Nombre"),
            'descripcionProyecto': ("Descripción"),
            'm2PorProyecto': ("Metros Cuadrados"),
            }
    

ProyectoFormSet = inlineformset_factory(Macroproyecto,Proyecto,form=ProyectoForm,extra=1,exclude=('macroproyecto',), labels={
            'nombreProyecto': ("Nombre"),
            'descripcionProyecto': ("Descripción"),
            'm2PorProyecto': ("Metros Cuadrados"),
            }, can_delete=True)

class VentaForm(forms.ModelForm):
    """Form definition for Venta."""

    class Meta:
        """Meta definition for Ventaform."""

        model = Venta
        exclude = (
            'volumenTotalVenta',
            'volumenInicialesVenta',
            'reajusteVenta',
            'subetapa'
            )
        labels = {
            'velocidadVentas': _('Velocidad (Tasa) de Ventas'),
            'porcentajeTopeRemanenteVentas': _('% Máximo (tope) de Remanente de Ventas'),
            'velocidadUltimasVentas': _('Velocidad (Tasa) de Últimas Ventas'),
            'porcentajeTopeInicialVentas': _('% Máximo (tope) de Ventas iniciales '),
            'porcentajeVelocidadInicialVentas': _('% Velocidad (Tasa) de Ventas iniciales '),
            'fechaInicioVentas': _('Fecha de Inicio de Ventas'),
            'numeroDeIncrementos': _('Cantidad de Incrementos'),
            'porcenReajusteIncremento': _('% de Reajuste en cada incremento'),
            'tipoIncremento': _('Tipo de Incremento'),
            'porcenTopeReajusteIncremento': _('% Tope de Reajuste de Incrementos'),
        }

VentaFormSet = inlineformset_factory(SubEtapa, Venta, form=VentaForm, extra=1, can_delete=True)        

class EtapaForm(forms.ModelForm):
    """Form definition for Etapa."""

    class Meta:
        """Meta definition for Etapaform."""

        model = Etapa        
        exclude = (
                'proyectoEtapa',
                'numeroTipoInmueble2Etapa',
                )
        labels = {
            'nombreEtapa': _('Nombre'),
            'descripcionEtapa': _('Descripción'),
            'numeroTipoInmuebleEtapa': _('Número Inmuebles'),
        }
        widgets = {
            'descripcionEtapa' : forms.Textarea(),
        }

EtapaFormSet = inlineformset_factory(Proyecto, Etapa, form=EtapaForm, extra=1, can_delete=True)

class SubEtapaForm(forms.ModelForm):
    """Form definition for SubEtapa."""

    class Meta:
        """Meta definition for SubEtapaform."""

        model = SubEtapa
        exclude = (
                'etapa',
                )
        labels = {
            'nombreSubEtapa': _('Nombre'),
            'descripcionSubEtapa': _('Descripción'),
        }
        widgets = {
            'descripcionSubEtapa' : forms.Textarea(),
        }

SubEtapaFormSet = inlineformset_factory(Etapa, SubEtapa, form=SubEtapaForm, extra=1, can_delete=True)

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









