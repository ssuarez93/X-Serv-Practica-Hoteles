# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0017_auto_20160520_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alojamiento',
            name='email',
            field=models.CharField(default=b'', max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alojamiento',
            name='telefono',
            field=models.CharField(max_length=20),
            preserve_default=True,
        ),
    ]
