# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-16 22:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0004_auto_20171211_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='macroproyecto',
            name='lote',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='lote', serialize=False, to='inmueble.Lote'),
        ),
    ]