# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-07 00:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inmueble', '0002_auto_20171102_0216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='areaBrutaLote',
            field=models.DecimalField(decimal_places=3, max_digits=16),
        ),
        migrations.AlterField(
            model_name='lote',
            name='areaCesionTierraLote',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='lote',
            name='areaCesionViasLote',
            field=models.DecimalField(decimal_places=3, max_digits=16),
        ),
        migrations.AlterField(
            model_name='lote',
            name='valorLote',
            field=models.DecimalField(decimal_places=4, max_digits=20),
        ),
        migrations.AlterField(
            model_name='lote',
            name='valorM2Cesion',
            field=models.DecimalField(decimal_places=4, max_digits=20),
        ),
        migrations.AlterField(
            model_name='lote',
            name='valorTotalLote',
            field=models.DecimalField(decimal_places=4, max_digits=20),
        ),
        migrations.AlterField(
            model_name='tipoinmueble',
            name='valorM2TipoInmueble',
            field=models.DecimalField(decimal_places=4, max_digits=20),
        ),
        migrations.AlterField(
            model_name='tipoinmueble',
            name='valorSalariosMinTipoInmueble',
            field=models.DecimalField(decimal_places=2, max_digits=16),
        ),
    ]