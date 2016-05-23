# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0006_auto_20160516_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alojamiento',
            name='telefono',
            field=models.CharField(max_length=14),
            preserve_default=True,
        ),
    ]
