# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0015_auto_20160519_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='alojamiento',
            name='email',
            field=models.CharField(default=b'', max_length=20),
            preserve_default=True,
        ),
    ]
