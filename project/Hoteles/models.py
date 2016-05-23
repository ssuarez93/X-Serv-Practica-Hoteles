from django.db import models

# Create your models here.

class ConfiguracionUsuario(models.Model):
    user = models.CharField(max_length=10)
    titulo = models.TextField(default="Pagina de", blank=True)
    color = models.CharField(max_length=1, default='b')
    letra = models.IntegerField(default=12)

class Alojamiento(models.Model):
    nombre = models.CharField(max_length=64)
    email = models.CharField(max_length=40, default="")
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=100)
    descripcion = models.TextField()
    web = models.URLField()
    categoria = models.CharField(max_length=15)
    subcategoria = models.CharField(max_length=25)
    puntuacion = models.IntegerField(default=0)
    num_visitas = models.IntegerField(default=0)
    num_comentarios = models.IntegerField(default=0)

class Comentario(models.Model):
    contenido= models.TextField()
    fecha = models.DateTimeField()
    user = models.CharField(max_length=10)
    alojamiento_id = models.IntegerField(default=0)

class Imagenes(models.Model):
    alojamiento = models.CharField(max_length=64)
    url1 = models.URLField()
    url2 = models.URLField()
    url3 = models.URLField()
    url4 = models.URLField()
    url5 = models.URLField()

class AlojamientoEscogido(models.Model):
    user = models.CharField(max_length=10)
    alojamiento_id = models.IntegerField(default=0)
    fecha_eleccion = models.DateTimeField()
