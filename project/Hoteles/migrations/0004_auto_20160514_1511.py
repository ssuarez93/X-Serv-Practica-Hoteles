# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0003_auto_20160514_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alojamiento',
            name='telefono',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
