from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin



class InicioView(LoginRequiredMixin,TemplateView):
    template_name = 'index.html'
