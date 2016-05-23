# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0010_auto_20160517_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alojamiento',
            name='direccion',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]
