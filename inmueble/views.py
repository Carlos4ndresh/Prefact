from django.shortcuts import render
from django.http import HttpResponse
from inmueble.forms import NuevoLote
from models import Lote


''' def index(request):
    return render(request,'inmueble/inmueble.html')

def lote(request):
    formLote = NuevoLote()

    if request.method == 'POST':
        formLote = NuevoLote(request.POST)

        if formLote.is_valid():
            formLote.save(commit=True)
            return index(request)
        else:
            print("ERROR! Valide la form")
    
    return render(request,'inmueble/lote.html',{'formLote':formLote})
 '''
 
 class LotesList(ListView):
     model = Lote
     context_object_name = 'lotes'
     template_name=''