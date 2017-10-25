from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    test = {'testkey':'Parametros Page'}
    return render(request,'parametros/parametros.html',context=test)
