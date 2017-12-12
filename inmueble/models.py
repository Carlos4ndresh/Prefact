from django.db import models

''' clases de parámetros de inmueble y lote  '''
class ParametroInmueble(models.Model):
    nombreParametroInmueble = models.CharField(max_length=45, blank=False)
    valorParametroInmueble = models.CharField(max_length=45, blank=False)
    descripcionParametro = models.CharField(max_length=255, blank=True, null=True)
    m2MinimoParametroInmueble = models.IntegerField()

    def __str__(self):
        return "Lote {a}".format(a=self.nombreParametroInmueble)


class Lote(models.Model):
    nombreLote = models.CharField(max_length=50,unique=True)
    areaBrutaLote = models.DecimalField(max_digits=16,decimal_places=3,blank=False)
    areaCesionViasLote = models.DecimalField(max_digits=16, decimal_places=3, 
                                            blank=True, null=True, default=0)
    porcentajeCesionVerdesLote = models.DecimalField(max_digits=5,decimal_places=2,blank=True, null=True)
    areaCesionTierraLote = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    valorM2Cesion = models.DecimalField(max_digits=20,decimal_places=4)
    valorLote = models.DecimalField(max_digits=20,decimal_places=4)
    valorPorcentajeLote = models.DecimalField(max_digits=5, decimal_places=2, blank=True, 
                                                default=0, null=True)
    valorEnPorcentaje = models.BooleanField(default=False)
    porcentajeFinanciarLote = models.DecimalField(max_digits=5,decimal_places=2)
    mesesGraciaInteresesLote = models.IntegerField(blank=True, default=0)
    tasaInteresMensualLote = models.DecimalField(max_digits=5,decimal_places=2)
    mesesTotalesPagoLote = models.IntegerField()
    valorTotalLote = models.DecimalField(max_digits=20,decimal_places=4,blank=True, null=True)
    mesesDePagoLote = models.CharField(max_length=45, blank=False)

    def __str__(self):
        return "Inmueble {a}".format(a=self.nombreLote)



class PagoLote(models.Model):
    mesPagoLote = models.IntegerField()
    porcentajeMesPagoLote = models.DecimalField(max_digits=5,decimal_places=2)
    lote = models.ForeignKey(Lote, related_name='pagosLote', on_delete=models.PROTECT)

    def __str__(self):
        return "Mes de Pago {a} y porcentaje {b}".format(a=self.mesPagoLote,b=self.porcentajeMesPagoLote)


class TipoInmueble(models.Model):
    nombreTipoInmueble = models.CharField(max_length=45, unique=True)
    areaTipoInmueble = models.IntegerField()
    noUnidadesTipoInmueble = models.IntegerField()
    valorM2TipoInmueble = models.DecimalField(max_digits=20,decimal_places=4)
    secundarioTipoInmueble = models.BooleanField()
    paramInmueble = models.ForeignKey(ParametroInmueble, related_name='+', on_delete=models.PROTECT)
    valorSalariosMinTipoInmueble = models.DecimalField(max_digits=16,decimal_places=2)
    etapa = models.ForeignKey('proyecto.Etapa', related_name='+', on_delete=models.PROTECT)

    def __str__(self):
        return "Tipo Inmueble {a}".format(a=self.nombreTipoInmueble)
