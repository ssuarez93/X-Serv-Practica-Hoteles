# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0012_auto_20160518_2154'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracionUsuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=10)),
                ('titulo', models.TextField(default=b'Pagina de', blank=True)),
                ('color', models.CharField(default=b'w', max_length=1)),
                ('letra', models.IntegerField(default=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='alojamientoescogido',
            name='user',
            field=models.ForeignKey(to='Hoteles.ConfiguracionUsuario'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comentario',
            name='user',
            field=models.ForeignKey(to='Hoteles.ConfiguracionUsuario'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
    ]
