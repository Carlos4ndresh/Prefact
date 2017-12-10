from django.conf.urls import url
from inmueble import views

app_name = 'inmueble'

urlpatterns = [
    url(r'^$',views.index),
    url(r'^lote.html',views.lote,name='lote')
]
