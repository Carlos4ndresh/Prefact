from django.db import models
from inmueble import models as inmueble_models
from parametros import models as parametros_models

# Create your models here.

# Venta
# Incremento
# Etapa
# SubEtapa
# ProyeccionIPC
# TablaIPC

class Macroproyecto(models.Model):
    nombreMacroproyecto = models.CharField(max_length=45, blank=False)
    descripcionMacroproyecto = models.CharField(max_length=255, blank=True, null=True)
    m2Macroproyecto = models.IntegerField()
    lote = models.OneToOneField(inmueble_models.Lote,on_delete=models.PROTECT,primary_key=True,)

    def __str__(self):
        return "Macroproyecto {a}".format(a=self.nombreMacroproyecto)


class Proyecto(models.Model):
    nombreProyecto = models.CharField(max_length=255, blank=False,) 
    descripcionProyecto = models.CharField(max_length=255, blank=True, null=True)
    m2PorProyecto = models.IntegerField()
    macroproyecto = models.ForeignKey(Macroproyecto, related_name='+', on_delete=models.PROTECT)

    def __str__(self):
        return "Proyecto: {a}".format(a=self.nombreProyecto) 

class Venta(models.Model):
    velocidadVentas = models.IntegerField(blank=False)
    porcentajeTopeRemanenteVentas = models.DecimalField(max_digits=5,decimal_places=2)
    velocidadUltimasVentas = models.IntegerField()
    porcentajeTopeInicialVentas = models.DecimalField(max_digits=5,decimal_places=2)
    porcentajeVelocidadInicialVentas = models.DecimalField(max_digits=5,decimal_places=2)
    fechaInicioVentas = models.DateField(blank=False)
    proyecto = models.ForeignKey(Proyecto, related_name='proyecto', on_delete=models.PROTECT)
    volumenTotalVenta = models.DecimalField(max_digits=13,decimal_places=4)
    reajusteVenta = models.DecimalField(max_digits=13,decimal_places=4)
    volumenInicialesVenta = models.DecimalField(max_digits=13,decimal_places=4)


    def __str__(self):
        pass 

    def __unicode__(self):
        pass 

class Etapa(models.Model):
    nombreEtapa = models.CharField(max_length=45, blank=False)
    descripcionEtapa = models.CharField(max_length=255, blank=True, null=True)
    ''' Campos legacy no se tiene claro todavía si son necesarios '''
    numeroTipoInmuebleEtapa = models.IntegerField()
    numeroTipoInmueble2Etapa = models.IntegerField()
    tipoProyecto = models.ForeignKey(parametros_models.TipoProyecto, related_name='tipoProyecto', 
        on_delete=models.PROTECT)

    def __str__(self):
        pass 

    def __unicode__(self):
        pass 

