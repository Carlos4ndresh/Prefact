from django.db import models

# Create your models here.

class ParametroInmueble(models.Model):
    nombreParametroInmueble = models.CharField(max_length=45, blank=False)
    valorParametroInmueble = models.CharField(max_length=45, blank=False)
    descripcionParametro = models.CharField(max_length=255, blank=True, null=True)
    m2MinimoParametroInmueble = models.IntegerField()



class Lote(models.Model):
    areaBrutaLote = models.DecimalField(max_digits=8,decima_places=3,blank=False)
    areaCesionViasLote = models.DecimalField(max_digits=8,decima_places=3)
    porcentajeCesionVerdesLote = models.DecimalField(max_digits=5,decima_places=2)
    areaCesionTierraLote = models.DecimalField(max_digits=5,decima_places=2)
    valorM2Cesion = models.DecimalField(max_digits=13,decima_places=4)
    valorLote = models.DecimalField(max_digits=13,decima_places=4)
    valorPorcentajeLote = models.DecimalField(max_digits=5,decima_places=2)
    porcentajeFinanciarLote = models.DecimalField(max_digits=5,decima_places=2)
    mesesGraciaInteresesLote = models.IntegerField()
    tasaInteresMensualLote = models.DecimalField(max_digits=5,decima_places=2)
    mesesTotalesPagoLote = models.IntegerField()
    valorTotalLote = models.DecimalField(max_digits=13,decima_places=4)
    mesesDePagoLote = models.CharField(max_length=45, blank=False)


class PagoLote(models.Model):
    mesPagoLote = models.IntegerField()
    porcentajeMesPagoLote = models.DecimalField(max_digits=5,decima_places=2)
    lote = models.ForeignKeyField(Lote, related_name='pagosLote', on_delete=models.PROTECT)


class TipoInmueble(models.Model):
    areaTipoInmueble = models.IntegerField()
    noUnidadesTipoInmueble = models.IntegerField()
    valorM2TipoInmueble = models.DecimalField(max_digits=13,decima_places=4)
    secundarioTipoInmueble = models.BooleanField(initial=False)
    paramInmueble = models.ForeignKeyField(ParametroInmueble, related_name='', on_delete=models.PROTECT)
    

