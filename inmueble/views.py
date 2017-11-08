from django.shortcuts import render
from django.http import HttpResponse
from inmueble.forms import NuevoLote


def index(request):
    return render(request,'inmueble/inmueble.html')

def lote(request):
    formLote = NuevoLote()

    if request.method == 'POST':
        formLote = NuevoLote(request.POST)

        if formLote.is_valid():
            formLote.save(commit=True)
            return index(request)
        else:
            print("ERROR!")
    
    return render(request,'inmueble/lote.html',{'formLote':formLote})
