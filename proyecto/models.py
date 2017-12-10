from django.db import models
from inmueble import models as inmueble_models
from parametros import models as parametros_models

''' Clases de Etapas de prefactibilidad '''

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
    proyecto = models.ForeignKey(Proyecto, related_name='proyectoVenta', on_delete=models.PROTECT)
    volumenTotalVenta = models.DecimalField(max_digits=20,decimal_places=4)
    reajusteVenta = models.DecimalField(max_digits=20,decimal_places=4)
    volumenInicialesVenta = models.DecimalField(max_digits=20,decimal_places=4)


    def __str__(self):
        return "Velocidad de ventas Proyecto {a}, {b} unidades".format(a=self.proyecto.nombreProyecto,
        b=self.velocidadVentas) 

class Etapa(models.Model):
    nombreEtapa = models.CharField(max_length=45, blank=False)
    descripcionEtapa = models.CharField(max_length=255, blank=True, null=True)
    ''' Campos legacy no se tiene claro todavía si son necesarios '''
    numeroTipoInmuebleEtapa = models.IntegerField()
    numeroTipoInmueble2Etapa = models.IntegerField()
    tipoProyecto = models.ForeignKey(parametros_models.TipoProyecto, related_name='tipoProyecto', 
        on_delete=models.PROTECT)

    def __str__(self):
        return self.nombreEtapa

    def __unicode__(self):
        pass 

class SubEtapa(models.Model):
    nombreSubEtapa = models.CharField(max_length=45, blank=False)
    descripcionSubEtapa = models.CharField(max_length=255, blank=True, null=True)
    etapa = models.ForeignKey(Etapa, related_name='etapa', on_delete=models.PROTECT)

    def __str__(self):
        return "Subetapa {a} de etapa {b}".format(a=self.nombreSubEtapa,b=self.etapa.nombreEtapa) 

    def __unicode__(self):
        pass 

class Incremento(models.Model):
    numeroDeIncrementos = models.IntegerField(blank=False)
    ''' # Porcentaje Reajuste FACTOR INCREMENTO '''
    porcenReajusteIncremento = models.DecimalField(max_digits=5,decimal_places=2,blank=False)
    tipoIncremento = models.ForeignKey(parametros_models.TipoIncremento, related_name='tipoIncrementoIncr', 
        on_delete=models.PROTECT)
    proyecto = models.ForeignKey(Proyecto, related_name='proyectoIncremento', on_delete=models.PROTECT) 
    porcenTopeReajusteIncremento = models.DecimalField(max_digits=5,decimal_places=2,)

    def __str__(self):
        return "Incrementos para el proyecto {a}: {b}".format(a=self.proyecto.nombreProyecto,
            b=self.numeroDeIncrementos) 

    def __unicode__(self):
        pass

class ProyeccionIPC(models.Model):
    anosProyeccionIPC = models.IntegerField(blank=False)
    tasaBaseProyeccionIPC = models.DecimalField(max_digits=5,decimal_places=2,blank=False)
    proyecto = models.ForeignKey(Proyecto, related_name='proyectoProyeccion', on_delete=models.PROTECT)

    def __str__(self):
        return "Proyeccion IPC Proyecto {a}:{b}".format(a=self.proyecto.nombreProyecto,
            b=self.anosProyeccionIPC) 

    def __unicode__(self):
        pass 

class TablaIPC(models.Model):
    anoTablaIPC = models.IntegerField()
    ipcAnoTablaIPC = models.DecimalField(max_digits=5,decimal_places=2,blank=True, null=True)
    numeroInmueblesEntregados = models.IntegerField()
    proyeccionIPC = models.ForeignKey(ProyeccionIPC,related_name='proyeccionIPC',
        on_delete=models.PROTECT)

    def __str__(self):
        pass 

    def __unicode__(self):
        pass 

