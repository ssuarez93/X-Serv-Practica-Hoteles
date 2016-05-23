# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alojamiento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=32)),
                ('telefono', models.IntegerField()),
                ('direccion', models.CharField(max_length=32)),
                ('descripcion', models.TextField()),
                ('web', models.URLField()),
                ('identificador', models.IntegerField()),
                ('categoria', models.CharField(max_length=16)),
                ('subcategoria', models.IntegerField()),
                ('puntuacion', models.IntegerField()),
                ('num_visitas', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AlojamientoEscogido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_eleccion', models.DateTimeField()),
                ('alojamiento', models.ForeignKey(to='Hoteles.Alojamiento')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contenido', models.TextField()),
                ('fecha', models.DateTimeField()),
                ('alojamiento', models.ForeignKey(to='Hoteles.Alojamiento')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identificador', models.IntegerField()),
                ('titulo', models.TextField(default=b'Pagina de', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='comentario',
            name='user',
            field=models.ForeignKey(to='Hoteles.Usuario'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alojamientoescogido',
            name='user',
            field=models.ForeignKey(to='Hoteles.Usuario'),
            preserve_default=True,
        ),
    ]
