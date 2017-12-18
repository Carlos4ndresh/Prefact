# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-12 01:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inmueble', '0007_tipoinmueble_nombretipoinmueble'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='mesesGraciaInteresesLote',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='lote',
            name='valorPorcentajeLote',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='lote',
            name='valorTotalLote',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=20),
        ),
    ]