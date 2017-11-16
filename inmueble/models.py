from django.db import models

''' clases de parámetros de inmueble y lote  '''
class ParametroInmueble(models.Model):
    nombreParametroInmueble = models.CharField(max_length=45, blank=False)
    valorParametroInmueble = models.CharField(max_length=45, blank=False)
    descripcionParametro = models.CharField(max_length=255, blank=True, null=True)
    m2MinimoParametroInmueble = models.IntegerField()

    ''' def __str__(self):
        return self.
 '''


class Lote(models.Model):
    nombreLote = models.CharField(max_length=50,unique=True)
    areaBrutaLote = models.DecimalField(max_digits=16,decimal_places=3,blank=False)
    areaCesionViasLote = models.DecimalField(max_digits=16,decimal_places=3,blank=True, null=True)
    porcentajeCesionVerdesLote = models.DecimalField(max_digits=5,decimal_places=2,blank=True, null=True)
    areaCesionTierraLote = models.DecimalField(max_digits=10,decimal_places=2)
    valorM2Cesion = models.DecimalField(max_digits=20,decimal_places=4)
    valorLote = models.DecimalField(max_digits=20,decimal_places=4)
    valorPorcentajeLote = models.DecimalField(max_digits=5,decimal_places=2)
    porcentajeFinanciarLote = models.DecimalField(max_digits=5,decimal_places=2)
    mesesGraciaInteresesLote = models.IntegerField()
    tasaInteresMensualLote = models.DecimalField(max_digits=5,decimal_places=2)
    mesesTotalesPagoLote = models.IntegerField()
    valorTotalLote = models.DecimalField(max_digits=20,decimal_places=4)
    mesesDePagoLote = models.CharField(max_length=45, blank=False)


class PagoLote(models.Model):
    mesPagoLote = models.IntegerField()
    porcentajeMesPagoLote = models.DecimalField(max_digits=5,decimal_places=2)
    lote = models.ForeignKey(Lote, related_name='pagosLote', on_delete=models.PROTECT)


class TipoInmueble(models.Model):
    areaTipoInmueble = models.IntegerField()
    noUnidadesTipoInmueble = models.IntegerField()
    valorM2TipoInmueble = models.DecimalField(max_digits=20,decimal_places=4)
    secundarioTipoInmueble = models.BooleanField()
    paramInmueble = models.ForeignKey(ParametroInmueble, related_name='+', on_delete=models.PROTECT)
    valorSalariosMinTipoInmueble = models.DecimalField(max_digits=16,decimal_places=2)
    etapa = models.ForeignKey('proyecto.Etapa', related_name='+', on_delete=models.PROTECT)
