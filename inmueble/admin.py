from django.contrib import admin

# Register your models here.

from inmueble.models import ParametroInmueble
from inmueble.models import Lote
from inmueble.models import PagoLote
from inmueble.models import TipoInmueble

admin.site.register(ParametroInmueble)
admin.site.register(Lote)
admin.site.register(PagoLote)
admin.site.register(TipoInmueble)

