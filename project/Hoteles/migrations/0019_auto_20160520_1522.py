# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0018_auto_20160520_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alojamiento',
            name='categoria',
            field=models.CharField(max_length=15),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alojamiento',
            name='subcategoria',
            field=models.CharField(max_length=25),
            preserve_default=True,
        ),
    ]
