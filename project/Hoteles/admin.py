from django.contrib import admin

# Register your models here.

from models import ConfiguracionUsuario, Comentario, Alojamiento, AlojamientoEscogido

admin.site.register(ConfiguracionUsuario)
admin.site.register(Comentario)
admin.site.register(Alojamiento)
admin.site.register(AlojamientoEscogido)
