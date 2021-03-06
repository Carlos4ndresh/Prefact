from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from proyecto.forms import MacroproyectoForm, ProyectoForm, VentaForm, VentaFormSet
from inmueble.forms import CrearLoteForm, InventarioFormSet, TipoInmuebleForm, TipoInmuebleAutoForm
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from . import models
from inmueble import models as modelInm
from .forms import (
                    ProyectoFormSet, EtapaFormSet, SubEtapaFormSet, EtapaForm, SubEtapaForm, 
                    MacroProyectoAutoForm, MacroEtapaAutoForm, MacroSubEtapaAutoForm, VentaAutoForm
                    )
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView,FormView)
from django.views.generic.edit import FormMixin                                  
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin  
from django.core.exceptions import ValidationError
from django.forms import formset_factory,forms, inlineformset_factory, modelformset_factory
from django.utils.translation import ugettext_lazy as _

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
        return self.etapa().proyectoEtapa
    
    def etapa(self):
        return get_object_or_404(models.Etapa, pk=self.kwargs['pk'])

    def get_queryset(self):
        etapa = get_object_or_404(models.Etapa, pk=self.kwargs['pk'])
        queryset = models.SubEtapa.objects.filter(etapa=etapa)
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

    def get_context_data(self, **kwargs):
        context = super(MacroproyectoCreateAutoView, self).get_context_data(**kwargs)
        context['lote_form'] = self.lote_form
        context['proyecto_form'] = self.proyecto_form

        if self.request.POST:
            context['lote_form'] = CrearLoteForm(self.request.POST)
            context['proyecto_form'] = MacroProyectoAutoForm(self.request.POST)

        return context
    
    def form_valid(self,form):
        context = self.get_context_data()
        lote_form = context['lote_form']
        proyecto_form = context['proyecto_form']
        if form.is_valid() and lote_form.is_valid() and proyecto_form.is_valid():
            lote = lote_form.save(commit=False)
            macroproyecto = form.save(commit=False)
            try:
                lote.nombreLote = macroproyecto.nombreMacroproyecto
                lote.areaBrutaLote = macroproyecto.m2Macroproyecto
                lote.save()
                macroproyecto.lote = lote
                macroproyecto.save()
                
                numeroProyectos = proyecto_form.cleaned_data['numeroProyectos']  
                for x in range(numeroProyectos):
                    metros = (macroproyecto.m2Macroproyecto/numeroProyectos+1)
                    proyecto = models.Proyecto(
                        nombreProyecto=macroproyecto.nombreMacroproyecto+" "+str(x+1),
                        descripcionProyecto=macroproyecto.descripcionMacroproyecto+" "+str(x+1),
                        m2PorProyecto=metros,
                        macroproyecto=macroproyecto
                        )
                    proyecto.save()
                    messages.success(self.request,"Macroproyecto {} creado".format(macroproyecto.nombreMacroproyecto))
            except IntegrityError as excepcion:
                messages.error(self.request,"Error. Ya hay un macroproyecto llamado así {}, por favor ingrese otro nombre. Error: {}".format(macroproyecto.nombreMacroproyecto,excepcion))
                return self.render_to_response(self.get_context_data(form=form,lote_form=lote_form,proyecto_form=proyecto_form))            
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

    def macroproyecto(self):
        return get_object_or_404(models.Macroproyecto, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(MacroproyectoEtapasAutoView, self).get_context_data(**kwargs)
        proyectos = models.Proyecto.objects.filter(macroproyecto=self.macroproyecto()).order_by('nombreProyecto')
        etapaAuto_formset = formset_factory(MacroEtapaAutoForm,extra=proyectos.count(),max_num=proyectos.count(),can_delete=False,can_order=False)
        if self.request.POST:
            context['etapaslist'] = etapaAuto_formset(self.request.POST,initial=[
                {
                    'nombreProyecto': x.nombreProyecto, 
                    'idProyecto': x.pk 
                } for x in proyectos
            ],prefix='etapalist')
        else:
            context['etapaslist'] = etapaAuto_formset(initial=[
                { 'nombreProyecto': x.nombreProyecto, 
                 'idProyecto': x.pk } for x in proyectos
                ],prefix='etapalist')  
        return context
   
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        etapasList = context['etapaslist']
        if etapasList.is_valid():
            etapaCount = 0
            for form in etapasList:
                etapaCount += 1
                numeroEtapas = form.cleaned_data['numeroEtapas']
                proyecto = models.Proyecto.objects.get(pk=form.cleaned_data['idProyecto'])
                for i in range(numeroEtapas):
                    etapa = models.Etapa(
                            nombreEtapa="Etapa "+str(etapaCount),
                            descripcionEtapa=proyecto.macroproyecto.descripcionMacroproyecto+" Descripción Etapa "+str(etapaCount)+proyecto.nombreProyecto,
                            proyectoEtapa=proyecto)
                    etapa.save()
        else:
            return self.render_to_response(self.get_context_data(etapaslist=etapasList))
        return redirect('proyecto:createAutoMacro3',pk=self.macroproyecto().pk)
    
    def get_success_url(self):
        return redirect("proyecto:createAutoMacro3",pk=self.macroproyecto().pk)

    def form_invalid(self, etapaslist):
        return self.render_to_response(
                 self.get_context_data(etapaslist=etapaslist,
                                       )
        )

class MacroproyectoSubEtapasAutoView(LoginRequiredMixin,TemplateView):
    template_name = 'macroproyecto/macroproyecto_auto_subetapas.html'

    def macroproyecto(self):
        return get_object_or_404(models.Macroproyecto, pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super(MacroproyectoSubEtapasAutoView, self).get_context_data(**kwargs)
        etapas = models.Etapa.objects.filter(proyectoEtapa__macroproyecto=self.macroproyecto()).order_by('nombreEtapa')
        subEtapa_formset = formset_factory(MacroSubEtapaAutoForm,extra=etapas.count(),max_num=etapas.count(),can_delete=False,can_order=False)
        if self.request.POST:
            '''
                Aquí se asignan valores iniciales al formulario de creaciòn de subetapas, para así relacionar cada etapa
                con su respectivo nùmero de subetapas, està pendiente resolver el nombrado de estas
            '''
            context['subEtapasList'] = subEtapa_formset(self.request.POST, prefix='subEtapaList',initial=[
                {
                    'nombreEtapa': e.nombreEtapa,
                    'idEtapa': e.pk,
                } for e in etapas
            ])
        else:
            context['subEtapasList'] = subEtapa_formset(
                initial=[
                    {
                        'nombreEtapa': e.nombreEtapa,
                        'idEtapa': e.pk,
                    } for e in etapas
                ], prefix='subEtapaList'
            )
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        subEtapasList = context['subEtapasList']
        if subEtapasList.is_valid():
            subEtapaCount = 0
            for form in subEtapasList:
                subEtapaCount += 1
                numeroSubEtapas = form.cleaned_data['numeroSubEtapas']
                etapa = models.Etapa.objects.get(pk=form.cleaned_data['idEtapa'])                
                for i in range(numeroSubEtapas):
                    subEtapa = models.SubEtapa(
                        nombreSubEtapa=" SubEtapa "+str(subEtapaCount),
                        descripcionSubEtapa="Descripción SubEtapa "+str(subEtapaCount)+" Etapa "+etapa.nombreEtapa,
                        etapa=etapa
                    )
                    subEtapa.save()
        else:
            return self.render_to_response(self.get_context_data(subEtapasList=subEtapasList))
        return redirect('proyecto:createAutoMacro4',pk=self.macroproyecto().pk)        

    def get_success_url(self):
        return redirect("proyecto:createAutoMacro4",pk=self.macroproyecto().pk)        

    def form_invalid(self, subEtapasList):
        return self.render_to_response(
                 self.get_context_data(subEtapasList=subEtapasList,
                                       )
        )    

class MacroproyectoInventarioAutoView(LoginRequiredMixin,TemplateView):
    template_name = 'macroproyecto/macroproyecto_auto_ventas.html'

    def macroproyecto(self):
        return get_object_or_404(models.Macroproyecto, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(MacroproyectoInventarioAutoView, self).get_context_data(**kwargs)
        subEtapas = models.SubEtapa.objects.filter(etapa__proyectoEtapa__macroproyecto=self.macroproyecto()).order_by('nombreSubEtapa')
        InventarioAutoFormset = modelformset_factory(modelInm.TipoInmueble, form=TipoInmuebleAutoForm, can_delete=True,extra=subEtapas.count())
        if self.request.POST:            
            inventarioList = InventarioAutoFormset(self.request.POST,prefix='inventario') 
            for form in inventarioList:
                form.fields['subEtapa'].queryset = subEtapas
            context['inventarioList'] = inventarioList
        else:
            inventarioList = InventarioAutoFormset(queryset=modelInm.TipoInmueble.objects.none(), prefix='inventario',initial=[
                {
                    'subEtapa': s
                } for s in subEtapas
            ]) 
            for form in inventarioList:
                form.fields['subEtapa'].queryset = subEtapas
            context['inventarioList'] = inventarioList
        return context
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        inventarioList = context['inventarioList']
        if inventarioList.is_valid():
            inventarioList.save()
        else:
            return self.render_to_response(self.get_context_data(inventarioList=inventarioList))
        return redirect('proyecto:createAutoMacro5',pk=self.macroproyecto().pk)

    def get_success_url(self):
        return redirect("proyecto:createAutoMacro5",pk=self.macroproyecto().pk)        

    def form_invalid(self, inventarioList):
        return self.render_to_response(
                 self.get_context_data(inventarioList=inventarioList,
                                       )
        )   

class MacroproyectoIncrementosAutoView(LoginRequiredMixin,TemplateView):
    template_name = 'macroproyecto/macroproyecto_auto_incrementos.html'

    def get_context_data(self, **kwargs):
        context = super(MacroproyectoIncrementosAutoView, self).get_context_data(**kwargs)
        subEtapas = models.SubEtapa.objects.filter(etapa__proyectoEtapa__macroproyecto=self.macroproyecto()).order_by('nombreSubEtapa')
        IncrementoFormSet = modelformset_factory(models.Venta, form=VentaAutoForm, can_delete=True,extra=subEtapas.count())
        if self.request.POST:
            incrementoList = IncrementoFormSet(self.request.POST, prefix='incrementolist')
            for form in incrementoList:
                form.fields['subetapa'].queryset = self.subEtapas()
            context['incrementoList'] = incrementoList
        else:
            incrementoList = IncrementoFormSet(queryset=models.Venta.objects.none(), prefix='incrementolist',initial=[
                {
                    'subetapa': s
                } for s in subEtapas
            ])
            for form in incrementoList:
                form.fields['subetapa'].queryset = self.subEtapas()
            context['incrementoList'] = incrementoList
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        incrementoList = context['incrementoList']
        if incrementoList.is_valid():
            incrementoList.save()
        else:
            return self.render_to_response(self.get_context_data(incrementoList=incrementoList))
        return redirect('proyecto:prefactibilidad_view',pk=self.macroproyecto().pk)

    def get_success_url(self):
        return redirect("proyecto:prefactibilidad_view",pk=self.macroproyecto().pk)        

    def form_invalid(self, incrementoList):
        return self.render_to_response(
                 self.get_context_data(incrementoList=incrementoList,
                                       )
        )  
    
    def macroproyecto(self):
        return get_object_or_404(models.Macroproyecto, pk=self.kwargs['pk'])

    def subEtapas(self):
        return  models.SubEtapa.objects.filter(etapa__proyectoEtapa__macroproyecto=self.macroproyecto()).order_by('nombreSubEtapa')

    

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