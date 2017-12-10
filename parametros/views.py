from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import (View,TemplateView,
                                ListView,DetailView,
                                CreateView,DeleteView,
                                UpdateView)

# Create your views here.

''' def index(request):
    test = {'testkey':'Parametros Page'}
    return render(request,'parametros/parametros.html',context=test) '''

class IndexParametrosView(TemplateView):
    template_name = 'parametros/parametros.html'

