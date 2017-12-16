from django.conf.urls import url
from proyecto import views

app_name = 'proyecto'

urlpatterns = [
    # url(r'^$',views.ProyectoIndexView.as_view(),name='indexProyecto'),
    url(r'^$',views.MacroproyectoListView.as_view(),name='indexProyecto'),
    url(r'^proyecto/nuevo/$',views.MacroproyectoCreateView.as_view(),name='nuevoMacro'),
]
