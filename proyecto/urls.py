from django.conf.urls import url
from proyecto import views

app_name = 'proyecto'

urlpatterns = [
    url(r'^$',views.ProyectoIndexView.as_view(),name='indexProyecto'),
    # url(r'^proyecto.html',views.proyecto,name='proyectos'),
]
