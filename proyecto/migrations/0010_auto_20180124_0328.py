# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-24 03:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0009_auto_20180117_0319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etapa',
            name='tipoProyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='etapa', to='parametros.TipoProyecto'),
        ),
        migrations.AlterField(
            model_name='macroproyecto',
            name='lote',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='macroproyecto', serialize=False, to='inmueble.Lote'),
        ),
        migrations.AlterField(
            model_name='proyeccionipc',
            name='proyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='proyeccionIPC', to='proyecto.Proyecto'),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='macroproyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='proyectos', to='proyecto.Macroproyecto'),
        ),
        migrations.AlterField(
            model_name='subetapa',
            name='etapa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subetapa', to='proyecto.Etapa'),
        ),
        migrations.AlterField(
            model_name='tablaipc',
            name='proyeccionIPC',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tablaIPC', to='proyecto.ProyeccionIPC'),
        ),
        migrations.AlterField(
            model_name='venta',
            name='proyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='venta', to='proyecto.Proyecto'),
        ),
        migrations.AlterField(
            model_name='venta',
            name='tipoIncremento',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='ventaIncremento', to='parametros.TipoIncremento'),
        ),
    ]
