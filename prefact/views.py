from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

class InicioView(TemplateView):
    template_name = 'index.html'
