# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-12 01:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inmueble', '0008_auto_20171212_0130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='areaCesionTierraLote',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='lote',
            name='areaCesionViasLote',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=16, null=True),
        ),
        migrations.AlterField(
            model_name='lote',
            name='valorPorcentajeLote',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='lote',
            name='valorTotalLote',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True),
        ),
    ]
