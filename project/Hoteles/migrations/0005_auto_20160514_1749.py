# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0004_auto_20160514_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alojamiento',
            name='telefono',
            field=models.CharField(max_length=14),
            preserve_default=True,
        ),
    ]
