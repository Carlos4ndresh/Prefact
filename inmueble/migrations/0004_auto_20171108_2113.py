# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-08 21:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inmueble', '0003_auto_20171107_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='areaCesionViasLote',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=16, null=True),
        ),
        migrations.AlterField(
            model_name='lote',
            name='porcentajeCesionVerdesLote',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
