from django.conf.urls import url
from proyecto import views

app_name = 'proyecto'

urlpatterns = [
    # url(r'^$',views.ProyectoIndexView.as_view(),name='indexProyecto'),
    url(r'^$',views.MacroproyectoListView.as_view(),name='indexProyecto'),
    # url(r'^proyecto/nuevomacro/$',views.MacroproyectoCreateView.as_view(),name='nuevoMacro'),
    url(r'^nuevomacro/$',views.MacroproyectoCreateView.as_view(),name='nuevoMacro'),
    # url(r'^nuevoproyecto/$',views.ProyectoCreateView.as_view(),name='nuevoProy'),
]
