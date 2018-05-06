from django.conf.urls import url
from proyecto import views

app_name = 'proyecto'

urlpatterns = [
    url(r'^$',views.MacroproyectoListView.as_view(),name='indexProyecto'),
    url(r'^nuevomacro/$',views.MacroproyectoCreateView.as_view(),name='nuevoMacro'),
    url(r'^macroproydetalle/(?P<pk>\d+)/edit/$',views.MacroproyectoEditView.as_view(),name='macro_edit'),
    url(r'^proyecto/(?P<pk>\d+)/lista/$',views.ProyectoListView.as_view(),name='proyecto_list'),
    url(r'^proyecto/(?P<pk>\d+)/incrementos/create/$',views.VentaCreateView.as_view(),name='proyecto_incremento'),
    url(r'^proyecto/(?P<pk>\d+)/incrementos/edit/$',views.VentaUpdateView.as_view(),name='incremento_edit'),
    url(r'^proyecto/(?P<pk>\d+)/inventario/$',views.ProyectoInventarioView.as_view(),name='proyecto_inventario'),
    url(r'^proyecto/(?P<pk>\d+)/etapa/create/$',views.EtapaCreateView.as_view(),name='etapa_create'),
    url(r'^proyecto/(?P<pk>\d+)/etapa/edit/$',views.EtapaUpdateView.as_view(),name='etapa_edit'),
    url(r'^proyecto/(?P<pk>\d+)/etapa/list/$',views.EtapaListView.as_view(),name='etapa_list'),
    ## Crear vistas de subetapas
    url(r'^proyecto/etapa/(?P<pk>\d+)/subetapa/create/$',views.SubEtapaCreateView.as_view(),name='subetapa_create'),
    url(r'^proyecto/etapa/(?P<pk>\d+)/subetapa/edit/$',views.SubEtapaUpdateView.as_view(),name='subetapa_edit'),
    url(r'^proyecto/etapa/(?P<pk>\d+)/subetapa/list/$',views.SubEtapaListView.as_view(),name='subetapa_list'),
    ## Modificar por subetapa
    url(r'^proyecto/etapa/subetapa/(?P<pk>\d+)/inventario/$',views.InventarioCreateView.as_view(),name='inventario_create'),
    url(r'^proyecto/etapa/subetapa/(?P<pk>\d+)/inventario/edit/$',views.InventarioEditView.as_view(),name='inventario_edit'),
    url(r'^prefactibilidad/(?P<pk>\d+)/view/$',views.PrefactibilidadView.as_view(),name='prefactibilidad_view'),
]
