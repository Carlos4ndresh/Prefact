from django.conf.urls import url
from proyecto import views

app_name = 'proyecto'

urlpatterns = [
    url(r'^$',views.index),
    url(r'^proyecto.html',views.proyecto,name='proyecto'),
]
