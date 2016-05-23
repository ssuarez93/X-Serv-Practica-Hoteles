# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0020_imagenes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alojamiento',
            name='identificador',
        ),
    ]
