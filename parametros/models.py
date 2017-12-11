from django.db import models

# Create your models here.

'''
Clase de Parámetros Generales
'''
class Parametro(models.Model):
    nombreParametro = models.CharField(max_length=45, blank=False)
    descripcionParametro = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombreParametro 

'''
Clase de Parámetros de Proyecto
'''
class TipoProyecto(models.Model):
    nombreTipoProyecto = models.CharField(max_length=45, blank=False)
    descripcionTipoProyecto = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombreTipoProyecto

'''
Clase de Parámetros de Incrementos
'''
class TipoIncremento(models.Model):
    tipoIncremento = models.IntegerField()
    valorIncrementoTipoIncremento = models.IntegerField()
    descripcionTipoIncr = models.CharField(max_length=255, blank=True, null=True) 

    def __str__(self):
        return self.descripcionTipoIncr
