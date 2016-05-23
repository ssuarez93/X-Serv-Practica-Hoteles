# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0016_alojamiento_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alojamiento',
            name='identificador',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
