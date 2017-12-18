from django import forms 
from proyecto.models import (Proyecto, Macroproyecto, Venta, Etapa, 
                            SubEtapa, Incremento, ProyeccionIPC, TablaIPC)
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
    

ProyectoFormSet = inlineformset_factory(Macroproyecto,Proyecto,form=ProyectoForm, extra=5,exclude=('macroproyecto',))

''' class ProyectoFormSet(BaseFormSet):

    def clean(self):
        """
        Validación para impedir proyectos con nombres duplicados
        """
        if any(self.errors):
            return

        nombres = []
        duplicados = False

        for form in self.forms:
            if form.cleaned_data:
                nombre = form.cleaned_data['nombreProyecto']

 '''

class VentaForm(forms.ModelForm):
    """Form definition for Venta."""

    class Meta:
        """Meta definition for Ventaform."""

        model = Venta
        # fields = ('',)
        fields = '__all__'

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

class IncrementoForm(forms.ModelForm):
    """Form definition for Incremento."""

    class Meta:
        """Meta definition for Incrementoform."""

        model = Incremento
        # fields = ('',)
        fields = '__all__'

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









