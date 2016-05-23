# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0007_auto_20160516_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='alojamiento',
            name='num_comentarios',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alojamiento',
            name='identificador',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alojamiento',
            name='num_visitas',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alojamiento',
            name='puntuacion',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alojamiento',
            name='subcategoria',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
