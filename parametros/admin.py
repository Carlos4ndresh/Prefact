from django.contrib import admin

# Register your models here.

from .models import Parametro
from .models import TipoProyecto
from .models import TipoIncremento

admin.site.register(Parametro)
admin.site.register(TipoProyecto)
admin.site.register(TipoIncremento)

