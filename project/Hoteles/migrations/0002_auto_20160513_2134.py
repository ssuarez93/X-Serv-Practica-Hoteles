# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alojamiento',
            name='direccion',
            field=models.CharField(max_length=64),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alojamiento',
            name='nombre',
            field=models.CharField(max_length=64),
            preserve_default=True,
        ),
    ]
