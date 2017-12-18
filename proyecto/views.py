from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from proyecto.forms import MacroproyectoForm, ProyectoForm
from django.forms import BaseInlineFormSet, inlineformset_factory
from inmueble.forms import CrearLoteForm
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from . import models
from .forms import ProyectoFormSet
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from django.db import transaction
                                  



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
    fields = ['nombreProyecto','descripcionProyecto','m2PorProyecto']
    # template_name = "TEMPLATE_NAME"
    # proy = models.Proyecto()
    # proy_form = ProyectoForm()
    # ProyectoFormSet = inlineformset_factory(models.Macroproyecto,model, form=ProyectoForm, exclude=('macroproyecto',), min_num=1,extra=3)
    
    # formsetIn = ProyectoFormSet(instance=proy)

'''     def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["macroproyecto"] = get_object_or_404(models.Macroproyecto, pk=self.request.session['macroproyID'])
        print("joder")
        if self.request.POST:
            context['lista_proyectos'] = ProyectoFormSet(self.request.POST)
        else:
            context['lista_proyectos'] = ProyectoFormSet()
        return context

    def form_valid(self,form):
        context = self.get_context_data(**kwargs)
        macroproyecto = context["macroproyecto"]
        print("pase por aquí {a}"+macroproyecto)
        lista_proyectos = context['lista_proyectos']
        if lista_proyectos.is_valid():
            print(macroproyecto)
            lista_proyectos.instance = macroproyecto
            print(lista_proyectos)
            lista_proyectos.save()
        return super(ProyectoCreateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('proyecto:indexProyecto') '''

class MacroproyectoListView(ListView):
    template_name = 'macroproyecto/macroproyecto_list.html'
    model = models.Macroproyecto    

class MacroproyectoCreateView(SuccessMessageMixin, CreateView):
    template_name = 'macroproyecto/macroproyecto_create.html'
    form_class = MacroproyectoForm
    model = models.Macroproyecto
    second_form_class = CrearLoteForm
    success_message = 'Proyecto Creado Exitosamente!'

    def get_context_data(self, **kwargs):
        context = super(MacroproyectoCreateView, self).get_context_data(**kwargs)
        context['lote_form'] = self.second_form_class
        if self.request.POST:
            context['lista_proyectos'] = ProyectoFormSet(self.request.POST)
        else:
            context['lista_proyectos'] = ProyectoFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()        
        lista_proyectos = context['lista_proyectos']
        lote_form = CrearLoteForm(self.request.POST)
        '''         if lote_form.is_valid():
            lote = lote_form.save()
            macroproyecto = form.save(commit=False)
            # print(lote)
            macroproyecto.lote = lote
            # print(macroproyecto.lote)
            macroproyecto.save()
            # self.request.session['macroproyID'] = macroproyecto.pk
        return super(MacroproyectoCreateView, self).form_valid(form) '''
        if lote_form.is_valid():
            lote = lote_form.save()
            macroproyecto = form.save(commit=False)
            print(lote)
            macroproyecto.lote = lote
            print(macroproyecto.lote)
            macroproyecto.save()
            if lista_proyectos.is_valid():
                lista_proyectos.instance = macroproyecto
                lista_proyectos.save()
            else:
                return self.render_to_response(self.get_context_data(form=form,lista_proyectos=lista_proyectos))
            self.request.session['macroproyID'] = macroproyecto.pk
        return super(MacroproyectoCreateView, self).form_valid(form)

    def form_invalid(self, form, lista_proyectos):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.

        Args:
            form: Assignment Form
            assignment_question_form: Assignment Question Form
        """
        return self.render_to_response(
                 self.get_context_data(form=form,
                                       lista_proyectos=lista_proyectos
                                       )
        )

    def get_success_url(self):
        # return reverse("proyecto:nuevoProy")
        return reverse("proyecto:indexProyecto")