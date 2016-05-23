# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0021_remove_alojamiento_identificador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracionusuario',
            name='color',
            field=models.CharField(default=b'b', max_length=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='configuracionusuario',
            name='letra',
            field=models.IntegerField(default=12),
            preserve_default=True,
        ),
    ]
