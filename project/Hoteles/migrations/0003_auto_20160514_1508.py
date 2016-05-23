# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0002_auto_20160513_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alojamiento',
            name='telefono',
            field=models.DecimalField(max_digits=12, decimal_places=12),
            preserve_default=True,
        ),
    ]
