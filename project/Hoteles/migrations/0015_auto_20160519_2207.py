# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0014_auto_20160519_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alojamiento',
            name='categoria',
            field=models.CharField(max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alojamiento',
            name='identificador',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alojamiento',
            name='subcategoria',
            field=models.CharField(max_length=20),
            preserve_default=True,
        ),
    ]
