from django.conf.urls import url
from proyecto import views

app_name = 'proyecto'

urlpatterns = [
    url(r'^$',views.MacroproyectoListView.as_view(),name='indexProyecto'),
    # url(r'^proyecto/nuevomacro/$',views.MacroproyectoCreateView.as_view(),name='nuevoMacro'),
    url(r'^nuevomacro/$',views.MacroproyectoCreateView.as_view(),name='nuevoMacro'),
    url(r'^macroproydetalle/(?P<pk>\d+)/edit/$',views.MacroproyectoEditView.as_view(),name='macro_edit'),
    # url(r'^proyecto/$',views.ProyectoListView.as_view(),name='proyecto_lista'),
    # url(r'^proyecto/(?P<pk>\d+)/incrementos/$',views.ProyectoIncrementoView.as_view(),name='proyecto_incremento'),
    url(r'^proyecto/(?P<pk>\d+)/lista/$',views.ProyectoListView.as_view(),name='proyecto_list'),
    url(r'^proyecto/(?P<pk>\d+)/incrementos/create/$',views.VentaCreateView.as_view(),name='proyecto_incremento'),
    url(r'^proyecto/(?P<pk>\d+)/incrementos/edit/$',views.VentaUpdateView.as_view(),name='incremento_edit'),
    url(r'^proyecto/(?P<pk>\d+)/inventario/$',views.ProyectoInventarioView.as_view(),name='proyecto_inventario'),
]
