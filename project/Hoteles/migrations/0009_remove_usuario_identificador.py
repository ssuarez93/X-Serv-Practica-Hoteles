# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0008_auto_20160517_2131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='identificador',
        ),
    ]
