# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0011_auto_20160517_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='color',
            field=models.CharField(default=b'w', max_length=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usuario',
            name='letra',
            field=models.IntegerField(default=10),
            preserve_default=True,
        ),
    ]
