from django.shortcuts import render
from django.http import HttpResponse
from inmueble.forms import NuevoLote


def index(request):
    return render(request,'inmueble/inmueble.html')

def lote(request):
    form = NuevoLote()

    if request.method == 'POST':
        form = NuevoLote(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print("ERROR!")
    
    return render(request,'inmueble/lote.html',{'form':form})
