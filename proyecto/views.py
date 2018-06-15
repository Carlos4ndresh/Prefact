from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from proyecto.forms import MacroproyectoForm, ProyectoForm, VentaForm, VentaFormSet
from inmueble.forms import CrearLoteForm, InventarioFormSet, TipoInmuebleForm
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from . import models
from inmueble import models as modelInm
from .forms import ProyectoFormSet, EtapaFormSet, SubEtapaFormSet, EtapaForm, SubEtapaForm, MacroProyectoAutoForm
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

class EtapaUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Etapa
    template_name = "proyecto/etapa_edit.html"
    form_class = EtapaForm

    def proyecto(self):
        return self.object.proyectoEtapa

    def macroproyecto(self):
        return self.object.proyectoEtapa.macroproyecto

    def get_context_data(self, **kwargs):
        context = super(EtapaUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['lista_subetapas'] = SubEtapaFormSet(self.request.POST, instance=self.object,prefix='subetapas')
        else:
            context['lista_subetapas'] = SubEtapaFormSet(instance=self.object,prefix='subetapas')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        lista_subetapas = context['lista_subetapas']
        if form.is_valid():
            etapa = form.save()
            if lista_subetapas.is_valid():
                lista_subetapas.instance = etapa
                lista_subetapas.save()
            else:
                return self.render_to_response(self.get_context_data(form=form,lista_subetapas=lista_subetapas))
        return super(EtapaUpdateView, self).form_valid(form)

    def get_success_url(self):
        return redirect('proyecto:etapa_list',pk=self.proyecto().pk).url


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


class SubEtapaCreateView(LoginRequiredMixin,TemplateView):
    template_name = "proyecto/subetapa_create.html"
    model = models.SubEtapa

    def proyecto(self):
        return self.etapa().proyectoEtapa
    
    def etapa(self):
        return get_object_or_404(models.Etapa, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(SubEtapaCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['lista_subetapas'] = SubEtapaFormSet(self.request.POST,prefix='subetapas')
        else:
            context['lista_subetapas'] = SubEtapaFormSet(prefix='subetapas')
        return context
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        lista_subetapas = context['lista_subetapas']
        if lista_subetapas.is_valid():
            lista_subetapas.instance = self.etapa()
            lista_subetapas.save()            
        return redirect('proyecto:etapa_list',pk=self.etapa().proyectoEtapa.pk)

    def get_success_url(self):
        return redirect('proyecto:etapa_list',pk=self.proyecto().proyectoEtapa.pk).url

class SubEtapaUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "proyecto/subetapa_edit.html"
    model = models.SubEtapa
    form_class = SubEtapaForm

    def proyecto(self):
        return self.object.etapa.proyectoEtapa
    
    def etapa(self):
        return self.object.etapa
    
    def get_success_url(self):
        return redirect('proyecto:subetapa_list',pk=self.etapa().pk).url


class SubEtapaListView(LoginRequiredMixin,ListView):
    template_name = "proyecto/subetapa_list.html"
    model = models.SubEtapa
    context_object_name = 'subetapa_list'

    def proyecto(self):
        return self.etapa.proyectoEtapa
    
    def etapa(self):
        return get_object_or_404(models.Etapa, pk=self.kwargs['pk'])

    def get_queryset(self):
        self.etapa = get_object_or_404(models.Etapa, pk=self.kwargs['pk'])
        queryset = models.SubEtapa.objects.filter(etapa=self.etapa)
        return queryset

class InventarioCreateView(LoginRequiredMixin,TemplateView):
    model = modelInm.TipoInmueble
    template_name = "proyecto/etapa_inventario.html"
    form_class = InventarioFormSet

    def subetapa(self):
        return get_object_or_404(models.SubEtapa,pk=self.kwargs['pk'])

    def etapa(self):
        return self.subetapa().etapa

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
            lista_inventario.instance = self.subetapa()
            lista_inventario.save()            
        return redirect('proyecto:etapa_list',pk=self.proyecto().pk)
    
   
    def get_success_url(self):
        return redirect('proyecto:etapa_list',pk=self.proyecto().pk).url            

class InventarioEditView(LoginRequiredMixin,TemplateView):
    model = modelInm.TipoInmueble
    template_name = "proyecto/etapa_inventario_edit.html"

    def subetapa(self):
        return get_object_or_404(models.SubEtapa,pk=self.kwargs['pk'])

    def etapa(self):
        return self.subetapa().etapa

    def proyecto(self):
        etapa = self.etapa()
        return etapa.proyectoEtapa

    def get_context_data(self, **kwargs):
        context = super(InventarioEditView, self).get_context_data(**kwargs)
        subetapa = self.subetapa()
        if self.request.POST:
            context['lista_inventario'] = InventarioFormSet(self.request.POST,instance=subetapa,prefix='inventarios')
        else:
            context['lista_inventario'] = InventarioFormSet(instance=subetapa,prefix='inventarios')
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        lista_inventario = context['lista_inventario']
        if lista_inventario.is_valid():
            lista_inventario.instance = self.subetapa()
            lista_inventario.save()            
        return redirect('proyecto:etapa_list',pk=self.proyecto().pk)
    
   
    def get_success_url(self):
        return redirect('proyecto:etapa_list',pk=self.proyecto().pk).url            

class VentaUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Venta
    template_name = "proyecto/incrementos_edit.html"
    form_class = VentaForm

    def proyecto(self):
        return self.object.subetapa.etapa.proyectoEtapa
    
    def subetapa(self):
        return get_object_or_404(models.SubEtapa, pk=self.kwargs['pk'])

    def get_object(self):
        subetapa = self.subetapa()
        return models.Venta.objects.get(subetapa__pk=self.kwargs['pk'])

    def get_success_url(self):
        return redirect('proyecto:subetapa_list',pk=self.subetapa().etapa.pk).url

class VentaCreateView(LoginRequiredMixin,FormView):
    model = models.Venta
    template_name = "proyecto/incrementos.html"
    form_class = VentaForm

    def proyecto(self):
        return self.subetapa().etapa.proyectoEtapa

    def subetapa(self):
        return get_object_or_404(models.SubEtapa, pk=self.kwargs['pk'])
    
    def get_success_url(self):
        return redirect('proyecto:subetapa_list',pk=self.subetapa().etapa.pk).url

    def form_valid(self, form):
        venta = form.save(commit=False)
        venta.subetapa = self.subetapa()
        venta.save()
        return super(VentaCreateView, self).form_valid(form) 

    


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
        lista_ventas = []
        proyecto_list = self.get_queryset()

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

class MacroproyectoCreateAutoView(LoginRequiredMixin,CreateView):
    template_name = 'macroproyecto/macroproyecto_auto.html'
    model = models.Macroproyecto
    form_class = MacroproyectoForm
    lote_form = CrearLoteForm
    proyecto_form = MacroProyectoAutoForm
    # venta_form = VentaForm
    # inventario_form = TipoInmuebleForm

    def get_context_data(self, **kwargs):
        context = super(MacroproyectoCreateAutoView, self).get_context_data(**kwargs)
        context['lote_form'] = self.lote_form
        context['proyecto_form'] = self.proyecto_form
        # context['venta_form'] = self.venta_form
        # context['inventario_form'] = self.inventario_form

        if self.request.POST:
            context['lote_form'] = CrearLoteForm(self.request.POST)
            context['proyecto_form'] = MacroProyectoAutoForm(self.request.POST)
            # context['venta_form'] = VentaForm(self.request.POST)
            # context['inventario_form'] = TipoInmuebleForm(self.request.POST)

        return context
    
    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     lote_form =  context['lote_form']
    #     etapas_form =  context['etapa_form']
    #     venta_form =  context['venta_form']
    #     inventario_form =  context['inventario_form']

    #     if lote_form.is_valid() and etapas_form.is_valid() and venta_form.is_valid() and inventario_form.is_valid():
    #         lote = lote_form.save(commit=False)
    #         macroproyecto = form.save(commit=False)
    #         lote.nombreLote = macroproyecto.nombreMacroproyecto
    #         lote.areaBrutaLote = macroproyecto.m2Macroproyecto
    #         lote.save()
    #         macroproyecto.lote = lote
    #         macroproyecto.save()
            
    #         numeroProyectos = etapas_form.cleaned_data['numeroProyectos']
    #         numeroEtapas = etapas_form.cleaned_data['numeroEtapas']
    #         numeroSubEtapas = etapas_form.cleaned_data['numeroSubEtapas']
    #         for x in range(numeroProyectos):
    #             metros = (macroproyecto.m2Macroproyecto/numeroProyectos+1)
    #             proyecto = models.Proyecto(
    #                 nombreProyecto=macroproyecto.nombreMacroproyecto+str(x+1),
    #                 descripcionProyecto=macroproyecto.descripcionMacroproyecto+str(x+1),
    #                 m2PorProyecto=metros,
    #                 macroproyecto=macroproyecto
    #                 )
    #             proyecto.save()
    #             for i in range(numeroEtapas):
    #                 etapa = models.Etapa(
    #                         nombreEtapa=macroproyecto.nombreMacroproyecto+str(x+1)+str(i+1),
    #                         descripcionEtapa=macroproyecto.descripcionMacroproyecto+str(x+1)+str(i+1),
    #                         proyectoEtapa=proyecto)
    #                 etapa.save()
    #                 for j in range(numeroSubEtapas):
    #                     subetapa = models.SubEtapa(
    #                             nombreSubEtapa=macroproyecto.nombreMacroproyecto+str(x+1)+str(i+1)+str(j+1),
    #                             descripcionSubEtapa=macroproyecto.descripcionMacroproyecto+str(x+1)+str(i+1)+str(j+1),
    #                             etapa=etapa
    #                         )
    #                     subetapa.save()
    #                     venta = venta_form.save(commit=False)
    #                     venta.pk = None
    #                     venta.subetapa = subetapa
    #                     venta.save()
    #                     inventario = inventario_form.save(commit=False)
    #                     inventario.pk = None
    #                     inventario.subEtapa = subetapa
    #                     inventario.save()
    #     else:
    #         return self.render_to_response(self.get_context_data(form=form,lote_form=lote_form,etapas_form=etapas_form,venta_form=venta_form,inventario_form=inventario_form))
    #     return super(MacroproyectoCreateAutoView, self).form_valid(form)
    def form_valid(self,form):
        context = self.get_context_data()
        lote_form = context['lote_form']
        proyecto_form = context['proyecto_form']
        if form.is_valid() and lote_form.is_valid() and proyecto_form.is_valid():
            lote = lote_form.save(commit=False)
            macroproyecto = form.save(commit=False)
            lote.nombreLote = macroproyecto.nombreMacroproyecto
            lote.areaBrutaLote = macroproyecto.m2Macroproyecto
            lote.save()
            macroproyecto.lote = lote
            macroproyecto.save()
            
            numeroProyectos = proyecto_form.cleaned_data['numeroProyectos']  
            for x in range(numeroProyectos):
                metros = (macroproyecto.m2Macroproyecto/numeroProyectos+1)
                proyecto = models.Proyecto(
                    nombreProyecto=macroproyecto.nombreMacroproyecto+str(x+1),
                    descripcionProyecto=macroproyecto.descripcionMacroproyecto+str(x+1),
                    m2PorProyecto=metros,
                    macroproyecto=macroproyecto
                    )
                proyecto.save()
        else:
            return self.render_to_response(self.get_context_data(form=form,lote_form=lote_form,proyecto_form=proyecto_form))
        return super(MacroproyectoCreateAutoView, self).form_valid(form) 
    
    def get_success_url(self):
        return redirect("proyecto:createAutoMacro2",pk=self.object.pk).url

    def form_invalid(self, form, lote_form,proyecto_form):
        return self.render_to_response(
                 self.get_context_data(form=form,
                                        lote_form=lote_form,
                                        proyecto_form=proyecto_form,
                                       )
        )

class MacroproyectoEtapasAutoView(LoginRequiredMixin,TemplateView):
    template_name = 'macroproyecto/macroproyecto_auto_etapas.html'

    def proyectos(self):
        self.macroproyecto = get_object_or_404(models.Macroproyecto, pk=self.kwargs['pk'])
        return models.Proyecto.objects.filter(macroproyecto=self.macroproyecto)

    def get_context_data(self, **kwargs):
        context = super(MacroproyectoEtapasAutoView, self).get_context_data(**kwargs)
        if self.request.POST:
            pass
        else:
            # context['lista_numero_etapas'] = EtapaAutoFormSet()
            pass
        return context
    
   
    def form_valid(self,form):
        context = self.get_context_data()
        
        if form.is_valid() and lote_form.is_valid() and proyecto_form.is_valid():
            lote = lote_form.save(commit=False)
            macroproyecto = form.save(commit=False)
            lote.nombreLote = macroproyecto.nombreMacroproyecto
            lote.areaBrutaLote = macroproyecto.m2Macroproyecto
            lote.save()
            macroproyecto.lote = lote
            macroproyecto.save()
            
            numeroProyectos = proyecto_form.cleaned_data['numeroProyectos']  
            for x in range(numeroProyectos):
                metros = (macroproyecto.m2Macroproyecto/numeroProyectos+1)
                proyecto = models.Proyecto(
                    nombreProyecto=macroproyecto.nombreMacroproyecto+str(x+1),
                    descripcionProyecto=macroproyecto.descripcionMacroproyecto+str(x+1),
                    m2PorProyecto=metros,
                    macroproyecto=macroproyecto
                    )
                proyecto.save()
        else:
            return self.render_to_response(self.get_context_data(form=form,lote_form=lote_form,proyecto_form=proyecto_form))
        return super(MacroproyectoCreateAutoView, self).form_valid(form) 
    
    def get_success_url(self):
        return reverse("proyecto:createAutoMacro2")

    def form_invalid(self, form, lote_form,proyecto_form):
        return self.render_to_response(
                 self.get_context_data(form=form,
                                        lote_form=lote_form,
                                        proyecto_form=proyecto_form,
                                       )
        )

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
            lote = lote_form.save(commit=False)
            macroproyecto = form.save(commit=False)
            lote.nombreLote = macroproyecto.nombreMacroproyecto
            lote.areaBrutaLote = macroproyecto.m2Macroproyecto
            lote.save()
            macroproyecto.lote = lote
            macroproyecto.save()
            if lista_proyectos.is_valid():
                lista_proyectos.instance = macroproyecto
                lista_proyectos.save()
            else:
                return self.render_to_response(self.get_context_data(form=form,lista_proyectos=lista_proyectos))
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


class ProyectoUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Proyecto
    template_name = "proyecto/proyecto_edit.html"
    form_class = ProyectoForm

    def macroproyecto(self):
        return self.object.macroproyecto


    def get_context_data(self, **kwargs):
        context = super(ProyectoUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['lista_etapas'] = EtapaFormSet(self.request.POST, instance=self.object,prefix='etapas')
        else:
            context['lista_etapas'] = EtapaFormSet(instance=self.object,prefix='etapas')
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()        
        lista_etapas = context['lista_etapas']
        if form.is_valid():
            proyecto = form.save()
            if lista_etapas.is_valid():
                lista_etapas.instance = proyecto
                lista_etapas.save()
            else:
                return self.render_to_response(self.get_context_data(form=form,lista_etapas=lista_etapas))
        return super(ProyectoUpdateView, self).form_valid(form)
    
    def get_success_url(self):
        return redirect("proyecto:proyecto_list",pk=self.macroproyecto().pk).url

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

        if lote_form.is_valid() and form.is_valid():
            
            macroproyecto = form.save()
            lote = lote_form.save(commit=False)
            lote.nombreLote = macroproyecto.nombreMacroproyecto
            lote.areaBrutaLote = macroproyecto.m2Macroproyecto
            lote.save()
            macroproyecto.lote = lote

            macroproyecto.save()
            
                        

            if lista_proyectos.is_valid():
                
                lista_proyectos.instance = self.object
                lista_proyectos.save()

            else:
                
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