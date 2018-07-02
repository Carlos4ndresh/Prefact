from django.db import models
from inmueble import models as inmueble_models
from parametros import models as parametros_models
from django.core.urlresolvers import reverse

''' Clases de Etapas de prefactibilidad '''

class Macroproyecto(models.Model):
    nombreMacroproyecto = models.CharField(max_length=255, blank=False)
    descripcionMacroproyecto = models.CharField(max_length=512, blank=True, null=True)
    m2Macroproyecto = models.IntegerField()
    lote = models.OneToOneField(inmueble_models.Lote,on_delete=models.PROTECT,primary_key=True,related_name='macroproyecto')

    def __str__(self):
        return "Macroproyecto {a}".format(a=self.nombreMacroproyecto)

    def get_absolute_url(self):        
        return reverse('macro_detail', kwargs={'pk': self.pk})

    def show_proyectos(self):
        return self.proyecto_set.all()[0]
    
    def is_macroproyecto_complete(self):

        tiposinmuebles = inmueble_models.TipoInmueble.objects.filter(subEtapa__etapa__proyectoEtapa__macroproyecto=self)
        ventas = Venta.objects.filter(subetapa__etapa__proyectoEtapa__macroproyecto=self)

        if tiposinmuebles and ventas:
            return True
        else:
            return False        



class Proyecto(models.Model):
    nombreProyecto = models.CharField(max_length=255, blank=False, unique=False) 
    descripcionProyecto = models.CharField(max_length=512, blank=True, null=True)
    m2PorProyecto = models.IntegerField()
    macroproyecto = models.ForeignKey(Macroproyecto, related_name='proyectos', on_delete=models.PROTECT)

    def __str__(self):
        return "Proyecto: {a}".format(a=self.nombreProyecto) 

    

class Venta(models.Model):
    velocidadVentas = models.IntegerField(blank=False)
    porcentajeTopeRemanenteVentas = models.DecimalField(max_digits=5,decimal_places=2)
    velocidadUltimasVentas = models.IntegerField()
    porcentajeTopeInicialVentas = models.DecimalField(max_digits=5,decimal_places=2)
    porcentajeVelocidadInicialVentas = models.DecimalField(max_digits=5,decimal_places=2)
    fechaInicioVentas = models.DateField(blank=False)
    volumenTotalVenta = models.DecimalField(max_digits=20,decimal_places=4,blank=True, null=True)
    reajusteVenta = models.DecimalField(max_digits=20,decimal_places=4,blank=True, null=True)
    volumenInicialesVenta = models.DecimalField(max_digits=20,decimal_places=4,blank=True, null=True)

    subetapa = models.ForeignKey('SubEtapa', related_name='ventas', on_delete=models.PROTECT,default=999999999)

    ## Datos de incrementos

    numeroDeIncrementos = models.IntegerField(null=True,blank=True)
    ''' # Porcentaje Reajuste FACTOR INCREMENTO '''
    porcenReajusteIncremento = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    tipoIncremento = models.ForeignKey(parametros_models.TipoIncremento, related_name='ventaIncremento', 
        on_delete=models.PROTECT, default=1)
    porcenTopeReajusteIncremento = models.DecimalField(max_digits=5,decimal_places=2,blank=True, null=True)


    def __str__(self):
        return "Velocidad de ventas Proyecto {a}, {b} unidades".format(a=self.proyecto.nombreProyecto,
        b=self.velocidadVentas) 

class Etapa(models.Model):
    nombreEtapa = models.CharField(max_length=255, blank=False)
    descripcionEtapa = models.CharField(max_length=512, blank=True, null=True)
    ''' Campos legacy no se tiene claro todavía si son necesarios '''
    numeroTipoInmuebleEtapa = models.IntegerField(blank=True, null=True)
    numeroTipoInmueble2Etapa = models.IntegerField(blank=True, null=True)
    proyectoEtapa = models.ForeignKey('Proyecto', related_name='etapas_proyecto', on_delete=models.PROTECT,default=999999999)

    def __str__(self):
        return self.nombreEtapa

    def __unicode__(self):
        pass 

class SubEtapa(models.Model):
    nombreSubEtapa = models.CharField(max_length=255, blank=False)
    descripcionSubEtapa = models.CharField(max_length=512, blank=True, null=True)
    etapa = models.ForeignKey(Etapa, related_name='subetapa', on_delete=models.PROTECT)

    def __str__(self):
        return "Subetapa {a} de etapa {b}".format(a=self.nombreSubEtapa,b=self.etapa.nombreEtapa) 

    def __unicode__(self):
        pass 
                

class ProyeccionIPC(models.Model):
    anosProyeccionIPC = models.IntegerField(blank=False)
    tasaBaseProyeccionIPC = models.DecimalField(max_digits=5,decimal_places=2,blank=False)
    subetapa = models.ForeignKey('SubEtapa', related_name='proyeccionIPC', on_delete=models.PROTECT,default=999999999)

    def __str__(self):
        return "Proyeccion IPC Proyecto {a}:{b}".format(a=self.proyecto.nombreProyecto,
            b=self.anosProyeccionIPC) 

    def __unicode__(self):
        pass 

class TablaIPC(models.Model):
    anoTablaIPC = models.IntegerField()
    ipcAnoTablaIPC = models.DecimalField(max_digits=5,decimal_places=2,blank=True, null=True)
    numeroInmueblesEntregados = models.IntegerField()
    proyeccionIPC = models.ForeignKey(ProyeccionIPC,related_name='tablaIPC',
        on_delete=models.PROTECT)

    def __str__(self):
        pass 

    def __unicode__(self):
        pass 

