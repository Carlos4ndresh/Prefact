from django.conf.urls import url
from parametros import views
 
app_name = 'parametros'

urlpatterns = [
    url(r'^$',views.IndexParametrosView,name='parametros')
]
