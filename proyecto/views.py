from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from proyecto.forms import MacroproyectoForm, ProyectoForm
# from django.forms.formsets import BaseFormSet, formset_factory
from django.forms import BaseInlineFormSet, inlineformset_factory
from inmueble.forms import CrearLoteForm
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from . import models
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)



# Create your views here.
''' def index(request):
   # return render(request,'inmueble/inmueble.html')
    return render(request,'proyecto/index.html')

def proyecto(request):
    formMacroProyecto = MacroproyectoForm()
    formProyecto = ProyectoForm()

    if request.method == 'POST':
        formMacroProyecto = MacroproyectoForm(request.POST)
        formProyecto = ProyectoForm(request.POST)

        if formMacroProyecto.is_valid():
            formMacroProyecto.save(commit=True)
            formProyecto.save(commit=True)
            return index(request)
        else:
            print("ERROR! Valide la form")
        

    contexto = {
        'macroproyectoForm' : formMacroProyecto,
        'proyectoForm' : formProyecto,
    } 
    
    return render(request,'proyecto/proyecto.html',contexto)
    
 '''
class ProyectoIndexView(ListView):
    model = models.Proyecto


class ProyectoCreateView(CreateView):
    model = models.Proyecto
    # template_name = "TEMPLATE_NAME"
    ProyectoFormSet = inlineformset_factory(models.Macroproyecto,model,exclude=('macroproyecto',))

    ''' def get_macroproyecto(self):
        macroPK = self.request.session['macroproyID']
        macroproyecto = get_object_or_404(models.Macroproyecto, pk=macroPK)
        return macroproyecto
    
    macroProyectoR = get_macroproyecto(ProyectoCreateView)
    formset = ProyectoFormSet(macroProyectoR) '''

    def form_valid(self,form):
        macroproyecto = get_object_or_404(models.Macroproyecto, pk=self.request.session[macroproyID])
        formset = ProyectoFormSet(instance=macroproyecto)
        if formset.is_valid():
            formset.save()
            return redirect('indexProyecto')


class MacroproyectoListView(ListView):
    template_name = 'macroproyecto/macroproyecto_list.html'
    model = models.Macroproyecto    

class MacroproyectoCreateView(SuccessMessageMixin, CreateView):
    template_name = 'macroproyecto/macroproyecto_create.html'
    form_class = MacroproyectoForm
    model = models.Macroproyecto
    second_form_class = CrearLoteForm
    success_message = 'Proyecto Creado Exitosamente!'
    # success_url = reverse_lazy('indexProyecto')
    # success_url = 'nuevoProy'

    def get_context_data(self, **kwargs):
        context = super(MacroproyectoCreateView, self).get_context_data(**kwargs)
        context['lote_form'] = self.second_form_class
        return context

    def form_valid(self, form):
        lote_form = CrearLoteForm(self.request.POST)
        if lote_form.is_valid():
            lote = lote_form.save()
            macroproyecto = form.save(commit=False)
            # print(lote)
            # macroproyecto.lote.id = lote.id
            macroproyecto.lote = lote
            # print(macroproyecto.lote)
            macroproyecto.save()
            self.request.session['macroproyID'] = macroproyecto.pk
        # return HttpResponseRedirect(self.get_success_url())
        # return HttpResponseRedirect('/proyecto')
        return super(MacroproyectoCreateView, self).form_valid(form)

    def get_success_url(self):
        return HttpResponseRedirect(reverse('nuevoProy'))