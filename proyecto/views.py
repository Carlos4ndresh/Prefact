from django.shortcuts import render
from django.http import HttpResponseRedirect
from proyecto.forms import MacroproyectoForm
from inmueble.forms import CrearLoteForm
from django.urls import reverse_lazy
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
''' class ProyectoIndexView(TemplateView):
    template_name = 'proyecto/proyecto.html'
 '''

class ProyectoIndexView(ListView):
    model = models.Proyecto

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
    success_url = '/proyecto'

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
        # return HttpResponseRedirect(self.get_success_url())
        return HttpResponseRedirect('/proyecto')