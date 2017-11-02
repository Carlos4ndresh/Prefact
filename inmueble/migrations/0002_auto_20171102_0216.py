# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 02:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('proyecto', '0001_initial'),
        ('inmueble', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipoinmueble',
            name='etapa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='proyecto.Etapa'),
        ),
        migrations.AddField(
            model_name='tipoinmueble',
            name='paramInmueble',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='inmueble.ParametroInmueble'),
        ),
        migrations.AddField(
            model_name='pagolote',
            name='lote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pagosLote', to='inmueble.Lote'),
        ),
    ]