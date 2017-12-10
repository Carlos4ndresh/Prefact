"""prefact URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
''' from parametros import views
from inmueble import views
from proyecto import views '''
from parametros.views import IndexParametrosView
import proyecto
import inmueble
from . import views

urlpatterns = [
    # url(r'^$',views.index,name='index'),
    url(r"^$", views.InicioView.as_view(), name="home"),
    # url(r'^parametros/',include('parametros.urls')),
    url(r'^parametros/', IndexParametrosView.as_view(), name="parametros"),
    # url(r'^inmueble/',include('inmueble.urls')),
    # url(r'^proyecto/',include('proyecto.urls')),
    url(r'^admin/', admin.site.urls),
]
