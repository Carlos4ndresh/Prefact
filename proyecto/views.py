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

class MacroproyectoEditView(UpdateView):
    template_name = 'macroproyecto/macroproyecto_detail.html'
    success_url = reverse_lazy("proyecto:indexProyecto")
    form_class = MacroproyectoForm
    model = models.Macroproyecto
    second_form_class = CrearLoteForm
    # success_message = 'Proyecto Creado Exitosamente!'

    def get_context_data(self, **kwargs):
        context = super(MacroproyectoEditView, self).get_context_data(**kwargs)
        # print(context)
        # context['lote_form'] = self.second_form_class
        # context['lote_form'] = CrearLoteForm(instance=context['macroproyecto'].lote)

        if self.request.POST:

            context['lista_proyectos'] = ProyectoFormSet(self.request.POST, instance=self.object)
            context['lote_form'] = CrearLoteForm(self.request.POST, instance=context['macroproyecto'].lote)

        else:
            
            context['lista_proyectos'] = ProyectoFormSet(instance=self.object)
            context['lote_form'] = CrearLoteForm(instance=context['macroproyecto'].lote)
            
        return context

    def form_valid(self, form):
        context = self.get_context_data()        
        lista_proyectos = context['lista_proyectos']

        # lote_form = CrearLoteForm(self.request.POST)
        lote_form = context['lote_form']

        print(lote_form)

        if lote_form.is_valid() and form.is_valid():
            print("poraqui1")            
            
            macroproyecto = form.save()
            macroproyecto.lote = lote_form.save()

            macroproyecto.save()
            
                        

            if lista_proyectos.is_valid():
                print("poraqui3")
                # lista_proyectos.instance = macroproyecto
                # lista_proyectos.save()

                lista_proyectos.instance = self.object
                lista_proyectos.save()

            else:
                
                print("poraqui2")
                return self.render_to_response(self.get_context_data(form=form,lote_form=lote_form,lista_proyectos=lista_proyectos))            

            return super(MacroproyectoEditView, self).form_valid(form)

        else:
            return self.render_to_response(self.get_context_data(form=form,lote_form=lote_form,lista_proyectos=lista_proyectos))
        # return super(MacroproyectoEditView, self).form_valid(form)

    def form_invalid(self, form, lote_form,lista_proyectos):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.

        Args:
            form: Assignment Form
            assignment_question_form: Assignment Question Form
        """
        print("aqui invalido")
        return self.render_to_response(
                 self.get_context_data(form=form,
                                        lote_form=lote_form,
                                       lista_proyectos=lista_proyectos
                                       )
        )