# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0013_auto_20160519_1345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alojamientoescogido',
            name='alojamiento',
        ),
        migrations.RemoveField(
            model_name='comentario',
            name='alojamiento',
        ),
        migrations.AddField(
            model_name='alojamientoescogido',
            name='alojamiento_id',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comentario',
            name='alojamiento_id',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alojamientoescogido',
            name='user',
            field=models.CharField(max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comentario',
            name='user',
            field=models.CharField(max_length=10),
            preserve_default=True,
        ),
    ]
