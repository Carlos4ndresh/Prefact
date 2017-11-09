from django.conf.urls import url
from proyecto import views

app_name = 'proyecto'

urlpatterns = [
    #url(r'^proyecto/$',views.index,name='proyecto'),
    url(r'^proyecto.html',views.proyecto,name='proyecto'),
]
