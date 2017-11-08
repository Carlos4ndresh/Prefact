from django.conf.urls import url
from inmueble import views

# app_name = 'inmueble'

urlpatterns = [
    url(r'^$',views.index),
]
