# -*- coding: utf-8 -*-

from django import forms
from models import Alojamiento, AlojamientoEscogido, ConfiguracionUsuario, Comentario
from django.template.loader import get_template
from django.template import Context, RequestContext
import xml_parser


filtros_categoria = (
    ('Hoteles', 'Hoteles'),
    ('Apartahoteles', 'Apartahoteles'),
    ('Hostales', 'Hostales'),
    ('Albergues', 'Albergues'),
    ('Residencias universitarias', 'Residencias Universitarias')
)

filtros_subcategoria = (
    ('Seleccione subcategoria', 'Seleccione subcategoria'),
    ('1 estrella', '1 estrella'),
    ('2 estrellas', '2 estrellas'),
    ('3 estrellas', '3 estrellas'),
    ('4 estrellas', '4 estrellas'),
    ('5 estrellas', '5 estrellas'),
    ('5 estrellas Gran Lujo', '5 estrellas Gran Lujo'),
    ('1 llave', '1 llave'),
    ('2 llaves', '2 llaves'),
    ('3 llaves', '3 llaves'),
    ('4 llaves', '4 llaves')
)

# Formulario para filtrar los alojamientos
class Filtrados(forms.Form):
    Categoria = forms.ChoiceField(choices=filtros_categoria)
    Subcategoria = forms.ChoiceField(choices=filtros_subcategoria)

# Formulario para filtrar alojamientos
def FormFiltrar():
    respuesta = '\n\t<FORM action="/alojamientos" name="filtrar" ' + \
                'method="POST" accept-charset="UTF-8">\n\t\t<fieldset>\t' + \
                '<legend>Filtrar alojamientos</legend>' + \
                '<input type="hidden" name="tipo" value="Filtrar" />' + Filtrados().as_p() + \
                '\n\t\t\t<input type="submit" value="Filtrar">\n\t\t</fieldset> \n\t</form><br>'
    return respuesta

# Función que filtra los alojamientos en función de su categoría y subcategoría
def FiltrarAlojamientos(request):
    alojamientos_filtrados = []
    alojamientos = Alojamiento.objects.filter(categoria=request.POST.get("Categoria"))
    # Recorro los alojamientos que cumplen el primer criterio en busca de que cumplan también el segundo
    if request.POST.get("Subcategoria") == 'Seleccione subcategoria':
        return alojamientos, 1
    else:
        for alojamiento in alojamientos:
            if alojamiento.subcategoria == request.POST.get("Subcategoria"):
                alojamientos_filtrados.append(alojamiento)
        return alojamientos_filtrados, 2

# Función que imprime los alojamientos filtrados
def ImprimirAloj(request, alojamientos, num):
    if int(num) == 2:
        respuesta = "<h3>" + str(request.POST.get("Categoria")) + " de " + \
                    str(request.POST.get("Subcategoria")) + " en Madrid:</h3><p>"
    elif int(num) == 1:
        respuesta = "<h3>" + str(request.POST.get("Categoria")) + " en Madrid:</h3><p>"
    for alojamiento in alojamientos:
        respuesta += "<li>" + str(alojamiento.nombre) + ": " + "<a href='/" + \
                    str(alojamiento.web) + "'>" + str(alojamiento.web) + "</a>"
    respuesta += '</p>'
    return respuesta



color_perfil = (
    ('b', 'marron'),
    ('y', 'amarillo'),
    ('g', 'verde'),
)

letra_perfil = (
    ('12', '12'),
    ('14', '14'),
    ('18', '18'),
)

class FormPerfil(forms.Form):
    color = forms.ChoiceField(choices=color_perfil)
    letra = forms.ChoiceField(choices=letra_perfil)

# Formulario para cambiar su tamaño de letra y su color
def FormPagina(user):
    respuesta = '\n\t<FORM action="/' + user + '" name="formpagina" ' + \
                'method="POST" accept-charset="UTF-8">\n\t\t' + \
                '<input type="hidden" name="tipo" value="pagina" />' + FormPerfil().as_p() + \
                '\n\t\t<input type="submit" value="Cambiar">\n\t</form><br>'
    return respuesta


class FormTitle(forms.Form):
    titulo = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'size': '14'}))

# Formulario para cambiar el titulo de la pagina
def FormTitulo(user):
    respuesta = '\n\t<FORM action="/' + user + '" name="formtitulo" ' + \
                'method="POST" accept-charset="UTF-8">\n\t\t' + \
                '<input type="hidden" name="tipo" value="titulo" />' + FormTitle().as_p() + \
                '\n\t\t<input type="submit" value="Cambiar">\n\t</form><br>'
    return respuesta


class Login(forms.Form):
    usuario = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'size': '2'}))
    contrasenia = forms.CharField(max_length=12, widget=forms.PasswordInput(attrs={'size': '2'}))

# Formulario para hacer login
def FormLogin(user):
    respuesta = '\n\t<FORM action="/' + user + '" name="login" ' + \
                'method="POST" accept-charset="UTF-8">\n\t\t' + \
                '<input type="hidden" name="tipo" value="cambiarperfil" />' + Login().as_p() + \
                '\n\t\t<input type="submit" value="Cambiar">\n\t</form><br>'
    return respuesta



# Formulario para actualizar el xml
def FormActualizar():
    respuesta = '\n\t<FORM action="/alojamientos" name = "actualizar" ' + \
                'method="POST" accept-charset="UTF-8">\n\t\t' + \
                '<input type="hidden" name="tipo" value="actualizar" />' + \
                '<input type="submit" value="Actualizar alojamientos">\n\t</form><br>'
    return respuesta


# Formulario para escribir un comentario
def FormComent(user, id):
    respuesta = '\n\t<FORM action="/alojamientos/' + str(id) + '" name=' + \
                '"elegiractform" method="POST" accept-charset="UTF-8">\n\t\t' + \
                '<input type="hidden" name="tipo" value="comentario" />' + \
                '<input type="hidden" name="usuario" value="' + user + '" />' + \
                '<textarea name="mensaje" rows="4" cols="40" ' + \
                'placeholder="Comentario..."></textarea>' + \
                '\n\t\t<br><input type="submit" value="Comentar">\n\t</form></br>'
    return respuesta


# Formulario para escoger una actividad
def FormEscogerAloj():
    respuesta = '\n\t<FORM action="" name = "escoger" ' + \
                'method="POST" accept-charset="UTF-8">\n\t\t' + \
                '<input type="hidden" name="tipo" value="escoger" />' + \
                '<input type="submit" value="Escoger alojamiento">\n\t</form><br>'
    return respuesta


# Menu de navegacion
def Menu(principal):
    salida = "<ul>\n"
    if not principal:
        salida += "<li><a href=/><span>Inicio</span></a></li>"
    salida += "<li><a href=/alojamientos><span>Todos</span></a></li>"
    salida += "<li><a href=/about><span>About US</span></a></li>"
    return salida


def PagUsers(users):
    adicional, titulo = ("", "")
    for user in users:
        if user.titulo == "Pagina de":
            titulo = "Pagina de " + str(user.user)
        else:
            titulo = user.titulo
        adicional += "<p class='link'><a href='/" + str(user.user) + "'>" + str(titulo) + \
                    "</a>" + ":   " + str(user.user) + "</p>"
    return adicional



opciones_idiomas = (
    ('2', 'Ingles'),
    ('3', 'Frances')
)

class Idiomas(forms.Form):
    Idioma = forms.ChoiceField(choices=opciones_idiomas)

def FormIdioma(id):
    respuesta = '\n\t<FORM action="/alojamientos/' + str(id) + '" name="idioma"' + \
                'method="POST" accept-charset="UTF-8">\n\t\t' + \
                '<input type="hidden" name="tipo" value="idioma" />' + Idiomas().as_p() + \
                '\n\t\t<input type="submit" value="Mostrar">\n\t</form><br>'
    return respuesta


def EnOtroIdioma(name, num):
    lista_alojamientos = xml_parser.parse(num) # Por defecto, 1 es español, 2 es inglés y 3 es francés
    (nombre, direc, email, telefono, descripcion, web) = ('', '', '', '', '', '')
    Encontrado = False
    for alojamiento in lista_alojamientos:
        if (alojamiento['name'] == name):
            print "ENTRO en True"
            Encontrado = True
            direc = alojamiento['address'] + '. ' + alojamiento['zipcode'] + '. ' + \
                    alojamiento['subAdministrativeArea'] + '. (' + alojamiento['latitude'] + ', ' + \
                    alojamiento['longitude'] + '). ' + alojamiento['country'] + '.'
            nombre = alojamiento['name']
            email = alojamiento['email']
            telefono = alojamiento['phone']
            descripcion = alojamiento['body']
            web = alojamiento['web']
    if Encontrado == False:
        print "ENTRO en False"
        nombre = 'error'
    return (nombre, direc, email, telefono, descripcion, web)




# Renderiza los parámetros que se le pasan
def Render(request, color, letra, titulo, navegacion, contenido, adicional):
    usuario = ""
    if request.user.is_authenticated():
        usuario = request.user.username
    template = get_template('WesternNightLights/index.html')
    visualizacion = RequestContext(request, {'titulo': titulo,
                            'color': color,
                            'letra': letra,
                            'usuario': usuario,
                            'form': Login(),
                            'menu_navegacion': navegacion,
                            'contenido': contenido,
                            'adicional': adicional,
                            'autenticado': request.user.is_authenticated()})
    rendered = template.render(visualizacion)
    return rendered


def info_about():
    contenido = "<h4>Esta pagina web alberga todos los alojamientos existentes en la ciudad de Madrid.</h4>" + \
                "<li>Si usted carga la pagina / encontrara los alojamientos ordenados por el numero de comentarios.</li>" + \
                "<li>Si usted accede a /alojamientos vera una lista con todos los alojamientos en la cual se puede\n" + \
                "realizar un filtrado en funcion de categoria y subcategoria.</li>" + \
                "<li>Si usted carga el /alojamientos/id accedera a la pagina personal de un alojamiento concreto.\n" + \
                "En esta pagina puede escoger un alojamiento para almacenarlo en su perfil, así como pedir que\n" + \
                "se muestre la informacion en otro idioma. Tambien se pueden realizar comentarios y leer los existentes</li>\n" + \
                "<li>Si usted accede a /usuario accederá a la información de alojamientos almacenada por el usuario.\n" + \
                "Si esta es su pagina personal podra cambiarle el titulo asi como el color o el tamaño de la letra</li>" + \
                "<li>Si usted accede a /usuario/xml vera la informacion del usuario en formato xml</li>\n" + \
                "<li>Si usted accede a /about obtendra la informacion que esta leyendo</li>"
    return contenido
