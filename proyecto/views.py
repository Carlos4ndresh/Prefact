from django.shortcuts import render
from proyecto.forms import *
from . import models
from django.views.generic import ListView, TemplateView


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
    # template_name = 'proyecto/proyecto.html'
    model = models.Proyecto

