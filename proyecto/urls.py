from django.conf.urls import url
from proyecto import views

app_name = 'proyecto'

urlpatterns = [
    url(r'^$',views.MacroproyectoListView.as_view(),name='indexProyecto'),
    # url(r'^proyecto/nuevomacro/$',views.MacroproyectoCreateView.as_view(),name='nuevoMacro'),
    url(r'^nuevomacro/$',views.MacroproyectoCreateView.as_view(),name='nuevoMacro'),
    # url(r'^nuevoproyecto/$',views.ProyectoCreateView.as_view(),name='nuevoProy'),
    # url(r'^macroproydetalle/(?P<pk>\d+)$',views.MacroproyectoDetailView.as_view(),name='macro_detail'),
    url(r'^macroproydetalle/(?P<pk>\d+)/edit/$',views.MacroproyectoEditView.as_view(),name='macro_edit'),
    url(r'^proyecto/(?P<pk>\d+)/incrementos/$',views.ProyectoListView.as_view(),name='proyecto_incremento'),
]
