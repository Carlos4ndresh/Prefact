from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from proyecto.forms import MacroproyectoForm, ProyectoForm, VentaForm
from inmueble.forms import CrearLoteForm, InventarioFormSet
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from . import models
from inmueble import models as modelInm
from .forms import ProyectoFormSet, EtapaFormSet
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView,FormView)
from django.views.generic.edit import FormMixin                                  
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin                                



# Create your views here.


class PrefactibilidadView(LoginRequiredMixin,TemplateView):
    template_name = "prefactibilidad/informe_lote.html"

    def macroproyecto(self):
        return get_object_or_404(models.Macroproyecto, pk=self.kwargs['pk'])


class ProyectoListView(LoginRequiredMixin,ListView):
    template_name = 'proyecto/proyecto_list.html'
    model = models.Proyecto

    def get_queryset(self):
        self.macroproyecto = get_object_or_404(models.Macroproyecto, pk=self.kwargs['pk'])
        return models.Proyecto.objects.filter(macroproyecto=self.macroproyecto)

    def macroproyecto(self):
        return get_object_or_404(models.Macroproyecto, pk=self.kwargs['pk'])

class EtapaListView(LoginRequiredMixin,ListView):
    model = models.Etapa
    context_object_name = 'etapa_list'
    template_name='proyecto/etapa_list.html' 

    def proyecto(self):
        return get_object_or_404(models.Proyecto, pk=self.kwargs['pk'])

    def get_queryset(self):
        self.proyecto = get_object_or_404(models.Proyecto, pk=self.kwargs['pk'])
        queryset = models.Etapa.objects.filter(proyectoEtapa=self.proyecto)
        return queryset

class EtapaUpdateView(LoginRequiredMixin,TemplateView):
    model = models.Etapa
    template_name = "proyecto/etapa_edit.html"

    def proyecto(self):
        return get_object_or_404(models.Proyecto, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(EtapaUpdateView, self).get_context_data(**kwargs)
        proyecto = self.proyecto()

        if self.request.POST:
            context['lista_etapas'] = EtapaFormSet(self.request.POST, instance=proyecto,prefix='etapas')
        else:            
            context['lista_etapas'] = EtapaFormSet(instance=proyecto,prefix='etapas')

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        lista_etapas = context['lista_etapas']
        if lista_etapas.is_valid():
            lista_etapas.instance = self.proyecto()
            lista_etapas.save()            
        return redirect('proyecto:proyecto_list',pk=self.proyecto().macroproyecto.pk)
    
    def get_success_url(self):
        return redirect('proyecto:proyecto_list',pk=self.proyecto().pk).url


class EtapaCreateView(LoginRequiredMixin,TemplateView):
    model = models.Etapa
    template_name = "proyecto/etapa_create.html"

    def proyecto(self):
        return get_object_or_404(models.Proyecto, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(EtapaCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['lista_etapas'] = EtapaFormSet(self.request.POST,prefix='etapas')
        else:
            context['lista_etapas'] = EtapaFormSet(prefix='etapas')
        return context
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        lista_etapas = context['lista_etapas']
        if lista_etapas.is_valid():
            lista_etapas.instance = self.proyecto()
            lista_etapas.save()            
        return redirect('proyecto:proyecto_list',pk=self.proyecto().macroproyecto.pk)

    def get_success_url(self):
        return redirect('proyecto:proyecto_list',pk=self.proyecto().macroproyecto.pk).url


class InventarioCreateView(LoginRequiredMixin,TemplateView):
    model = modelInm.TipoInmueble
    template_name = "proyecto/etapa_inventario.html"
    form_class = InventarioFormSet

    def etapa(self):
        return get_object_or_404(models.Etapa, pk=self.kwargs['pk'])

    def proyecto(self):
        etapa = self.etapa()
        return etapa.proyectoEtapa

    def get_context_data(self, **kwargs):
        context = super(InventarioCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['lista_inventario'] = InventarioFormSet(self.request.POST,prefix='inventarios')
        else:
            context['lista_inventario'] = InventarioFormSet(prefix='inventarios')
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        lista_inventario = context['lista_inventario']
        if lista_inventario.is_valid():
            lista_inventario.instance = self.etapa()
            lista_inventario.save()            
        return redirect('proyecto:etapa_list',pk=self.proyecto().pk)
    
   
    def get_success_url(self):
        return redirect('proyecto:proyecto_list',pk=self.proyecto().pk).url            

class InventarioEditView(LoginRequiredMixin,TemplateView):
    model = modelInm.TipoInmueble
    template_name = "proyecto/etapa_inventario_edit.html"

    def etapa(self):
        return get_object_or_404(models.Etapa, pk=self.kwargs['pk'])

    def proyecto(self):
        etapa = self.etapa()
        return etapa.proyectoEtapa

    def get_context_data(self, **kwargs):
        context = super(InventarioEditView, self).get_context_data(**kwargs)
        etapa = self.etapa()
        if self.request.POST:
            context['lista_inventario'] = InventarioFormSet(self.request.POST,instance=etapa,prefix='inventarios')
        else:
            context['lista_inventario'] = InventarioFormSet(instance=etapa,prefix='inventarios')
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        lista_inventario = context['lista_inventario']
        if lista_inventario.is_valid():
            lista_inventario.instance = self.etapa()
            lista_inventario.save()            
        return redirect('proyecto:etapa_list',pk=self.proyecto().pk)
    
   
    def get_success_url(self):
        return redirect('proyecto:proyecto_list',pk=self.proyecto().pk).url            

class VentaUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Venta
    template_name = "proyecto/incrementos_edit.html"
    form_class = VentaForm

    def proyecto(self):
        return get_object_or_404(models.Proyecto, pk=self.kwargs['pk'])

    def get_object(self):
        proyecto = get_object_or_404(models.Proyecto, pk=self.kwargs['pk'])
        return models.Venta.objects.get(proyecto__pk=self.kwargs['pk'])

    def get_success_url(self):
        return redirect('proyecto:proyecto_list',pk=self.proyecto().macroproyecto.pk).url

class VentaCreateView(LoginRequiredMixin,FormView):
    model = models.Venta
    template_name = "proyecto/incrementos.html"
    form_class = VentaForm

    def proyecto(self):
        return get_object_or_404(models.Proyecto, pk=self.kwargs['pk'])

    def form_valid(self, form):
        venta = form.save(commit=False)
        venta.proyecto = models.Proyecto.objects.get(pk=(self.kwargs['pk']))
        venta.save()
        return redirect('proyecto:proyecto_list',pk=venta.proyecto.macroproyecto.pk)


class MacroproyectoListView(LoginRequiredMixin,ListView):
    template_name = 'macroproyecto/macroproyecto_list.html'
    model = models.Macroproyecto    


class ProyectoInventarioView(LoginRequiredMixin,TemplateView):
    template_name = 'proyecto/proyecto_inventario.html'

class ProyectoIncrementoView(LoginRequiredMixin,TemplateView):
    template_name = 'proyecto/incremento_ventas.html'
    # form_class = VentaFormSet

    def get_queryset(self):
        self.macroproyecto = get_object_or_404(models.Macroproyecto, pk=self.kwargs['pk'])
        return models.Proyecto.objects.filter(macroproyecto=self.macroproyecto)

    def macroproyecto(self):
        return get_object_or_404(models.Macroproyecto, pk=self.kwargs['pk'])
    
    def lista_ventas(self):
        proyecto_list = self.get_queryset() 

        if self.request.POST:
            lista_ventas = []
            for proyecto in proyecto_list:
                formv = VentaFormSet(self.request.POST,instance=proyecto)
                lista_ventas.append(formv)
            return lista_ventas
        else:
            lista_ventas = []
            for proyecto in proyecto_list:
                formv = VentaFormSet(instance=proyecto)
                lista_ventas.append(formv)
            return lista_ventas

    def post(self, request, *args, **kwargs):
        # lista_ventas = VentaFormSet(self.request.POST)
        lista_ventas = []
        proyecto_list = self.get_queryset()
        # for proyecto in proyecto_list:
        #     formv = VentaFormSet(self.request.POST,instance=proyecto)
        #     lista_ventas.append(formv)
        #     # print(formv)
        #     print(self.request.POST)
        #     if formv.is_valid():
        #         formv.save()
        # if (lista_ventas.is_valid()):
        #     return self.form_valid(form, lista_ventas)
        return self.form_invalid(lista_ventas)

    def form_valid(self,lista_ventas):
        context = self.get_context_data()        
        if lista_ventas.is_valid():
            lista_ventas.save()
        else:
            return self.render_to_response(self.get_context_data(lista_ventas=lista_ventas))

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self,lista_ventas):
        """
        Called if whether a form is invalid. Re-renders the context
        data with the data-filled forms and errors.
        """
        # print(lista_ventas)
        return self.render_to_response(
            self.get_context_data(lista_ventas=lista_ventas)
        )
    
    def get_success_url(self):
        return reverse("proyecto:indexProyecto")

class MacroproyectoCreateView(LoginRequiredMixin,SuccessMessageMixin, CreateView):
    template_name = 'macroproyecto/macroproyecto_create.html'
    form_class = MacroproyectoForm
    model = models.Macroproyecto
    second_form_class = CrearLoteForm
    success_message = 'Proyecto Creado Exitosamente!'

    def get_context_data(self, **kwargs):
        context = super(MacroproyectoCreateView, self).get_context_data(**kwargs)
        context['lote_form'] = self.second_form_class
        if self.request.POST:
            context['lista_proyectos'] = ProyectoFormSet(self.request.POST,prefix='proyectos')
        else:
            context['lista_proyectos'] = ProyectoFormSet(prefix='proyectos')
        return context

    def form_valid(self, form):
        context = self.get_context_data()        
        lista_proyectos = context['lista_proyectos']
        lote_form = CrearLoteForm(self.request.POST)

        if lote_form.is_valid():
            lote = lote_form.save()
            macroproyecto = form.save(commit=False)
            macroproyecto.lote = lote
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

class MacroproyectoEditView(LoginRequiredMixin,UpdateView):
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

            context['lista_proyectos'] = ProyectoFormSet(self.request.POST, instance=self.object,prefix='proyectos')
            context['lote_form'] = CrearLoteForm(self.request.POST, instance=context['macroproyecto'].lote)

        else:
            
            context['lista_proyectos'] = ProyectoFormSet(instance=self.object,prefix='proyectos')
            context['lote_form'] = CrearLoteForm(instance=context['macroproyecto'].lote)
            
        return context

    def form_valid(self, form):
        context = self.get_context_data()        
        lista_proyectos = context['lista_proyectos']

        # lote_form = CrearLoteForm(self.request.POST)
        lote_form = context['lote_form']

        print(lote_form)

        if lote_form.is_valid() and form.is_valid():
            
            macroproyecto = form.save()
            macroproyecto.lote = lote_form.save()

            macroproyecto.save()
            
                        

            if lista_proyectos.is_valid():
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