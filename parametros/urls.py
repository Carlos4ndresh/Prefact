from django.conf.urls import url
from parametros import views


urlpatterns = [
    url(r'^$',views.index,name='index')
]
