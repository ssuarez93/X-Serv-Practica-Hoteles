# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0019_auto_20160520_1522'),
    ]

    operations = [
        migrations.CreateModel(
            name='Imagenes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alojamiento', models.CharField(max_length=64)),
                ('url1', models.URLField()),
                ('url2', models.URLField()),
                ('url3', models.URLField()),
                ('url4', models.URLField()),
                ('url5', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
