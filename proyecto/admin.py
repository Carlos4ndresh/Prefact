from django.contrib import admin

# Register your models here.

from proyecto.models import Macroproyecto
from proyecto.models import Proyecto
from proyecto.models import Venta
from proyecto.models import Etapa
from proyecto.models import SubEtapa
from proyecto.models import Incremento
from proyecto.models import ProyeccionIPC
from proyecto.models import TablaIPC

admin.site.register(Macroproyecto)
admin.site.register(Proyecto)
admin.site.register(Venta)
admin.site.register(Etapa)
admin.site.register(SubEtapa)
admin.site.register(Incremento)
admin.site.register(ProyeccionIPC)
admin.site.register(TablaIPC)
