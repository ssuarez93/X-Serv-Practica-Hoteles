#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt, CsrfViewMiddleware
from models import Alojamiento, AlojamientoEscogido, ConfiguracionUsuario, Comentario, Imagenes
import xml_parser
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from django.contrib import auth
import requests, sys, string, urllib, urllib2, os.path, math
from django.utils.encoding import smart_str, smart_unicode
from django.template.loader import get_template
from django.template import Context, RequestContext
from funciones import FormFiltrar, FiltrarAlojamientos, ImprimirAloj, FormActualizar
from funciones import Render, Menu, PagUsers, FormIdioma, EnOtroIdioma, info_about, Login
from funciones import FormComent, FormLogin, FormPagina, FormTitulo, FormEscogerAloj
from datetime import datetime

# Create your views here.


# Tras hacer login correcto
def login_correcto(request):
    # Redirijo a la página del usuario
    if request.method == 'POST':
        nombre = request.body.split("&")[1]
        contrasenia = request.body.split("&")[2]
        nombre = nombre.split("=")[1]
        contrasenia = contrasenia.split("=")[1]
        user = auth.authenticate(username = nombre, password = contrasenia)
        if user is not None:
			auth.login(request, user)
    return HttpResponseRedirect("/" + nombre)


# Muestra la pagina de un usuario
@csrf_exempt
def profile(request, user):
    # Para saber si muestro los 10 primeros, del 10 al 20 o qué hoteles escogidos
    try:
        offset = int(request.GET.get('offset'))
    except TypeError:
        offset = 0
    num = int(offset)*10
    form_titulo = FormTitulo(user)
    form_pagina = FormPagina(user)
    usuario = ConfiguracionUsuario.objects.get(user=user)
    titulo = usuario.titulo
    if titulo == "Pagina de":
        titulo = "Pagina de " + str(user)

    # Muestro hoteles escogidos por el usuario, si está logueado podrá cambiar color, letra y titulo
    if request.method == "GET":
        escogidos = AlojamientoEscogido.objects.filter(user=user)
        respuesta = ""
        for escogido in escogidos[num:num+10]:
            alojamiento = Alojamiento.objects.get(id=escogido.alojamiento_id)
            imagenes = Imagenes.objects.get(alojamiento=alojamiento.nombre)
            respuesta += "<br>" + str(escogido.fecha_eleccion) + ": " + \
                        "<a href='" + str(alojamiento.web) + "'>" + \
                        "</br>" + str(alojamiento.nombre) + "</a>" + "</br>" + \
                        '<img src="' + imagenes.url1 + '"width="200" height="150" border="2">' + \
                        "</br>" + alojamiento.direccion + "</br>" + "<a href='/" + "alojamientos/" + \
                        str(alojamiento.id) + "'>Mas informacion</a></br></br>"
        # Para mostrar enlace a los 10 siguientes
        contador = 0
        for escogido in escogidos:
            contador = contador +1
        for n in range (0, int(math.ceil(float(contador)/10.0))):
            respuesta += "<a href='" + str(user) + "?offset=" + str(n) + "'>" + str(n+1) + " " + "</a>"
        # Para mostrar formularios si está autenticado y es su pagina
        if request.user.is_authenticated():
            if str(request.user.username) == str(user):
                contenido = "<p>Bienvenido, esta dentro de su pagina de usuario.<p>"
                contenido += form_titulo + form_pagina + respuesta
            else:
                contenido = "<p>Estos son los alojamientos escogidos por este usuario: <p>"
                contenido += respuesta
        else:
            contenido = "<p>Estos son los alojamientos escogidos por este usuario: <p>"
            contenido += respuesta

    # Si es su pagina y está autenticado, recibo los datos de los cambios que quiere hacer u hotel escogido
    elif request.method == "POST":
        usuario = ConfiguracionUsuario.objects.get(user=user)
        id_usuario = usuario.id
        if request.POST.get("tipo") == "pagina":
            color = request.POST.get("color")
            letra = request.POST.get("letra")
            configuracion_nueva = ConfiguracionUsuario(id=id_usuario, user=user, color=color,
                                                        letra=letra, titulo=usuario.titulo)
            configuracion_nueva.save()
            contenido = "Perfil actualizado correctamente"
        elif request.POST.get("tipo") == "titulo":
            titulo = request.POST.get("titulo")
            if titulo != "":
                configuracion_nueva = ConfiguracionUsuario(id=id_usuario, user=user, color=usuario.color,
                                                            letra=usuario.letra, titulo=titulo)
                configuracion_nueva.save()
                contenido = "Perfil actualizado correctamente"
        else:
            contenido = "Ha ocurrido un error actualizando el perfil"
        return HttpResponseRedirect("/" + user)
    else:
        contenido = "Ha ocurrido un error con el metodo usado"

    # Para pasar los datos del menu de navegacion asi como el estilo de la pagina escogida
    navegacion = Menu(False)
    try:
        usuarios = ConfiguracionUsuario.objects.all()
        adicional = PagUsers(usuarios)
    except ConfiguracionUsuario.DoesNotExist:
        adicional = ""
    color, letra = ("b", 12)
    try:
        nombre = request.user
        user = ConfiguracionUsuario.objects.get(user=nombre)
        color = user.color
        letra = user.letra
    except ConfiguracionUsuario.DoesNotExist:
        None

    rendered = Render(request, color, letra, titulo, navegacion, contenido, adicional)
    return HttpResponse(rendered)


# Pagina principal con los hoteles con mas comentarios
def principal(request):
    try:
        offset = int(request.GET.get('offset'))
    except TypeError:
        offset = 0
    num = int(offset)*10
    form_act = FormActualizar()   # Actuallizar alojamientos

    if request.method == "GET":
        try:
            titulo = "Alojamientos más comentados:"
            lista_alojamientos = Alojamiento.objects.all().order_by('-num_comentarios')
            respuesta = form_act
            for alojamiento in lista_alojamientos[num:num+10]:
                if int(alojamiento.num_comentarios) > 0:
                    imagenes = Imagenes.objects.get(alojamiento=alojamiento.nombre)
                    respuesta += "</br>" + "<a href='" + str(alojamiento.web) + "'>" + \
                                "</br>" + str(alojamiento.nombre) + "</a>" + "</br>" + \
                                '<img src="' + imagenes.url1 + '"width="200" height="150" border="2">' + \
                                "</br>" + alojamiento.direccion + "</br>" + "<a href='/" + "alojamientos/" + \
                                str(alojamiento.id) + "'>Mas informacion</a></br>"
            # Para mostrar enlace a los 10 siguientes
            contador = 0
            for alojamiento in lista_alojamientos:
                if alojamiento.num_comentarios > 0:
                    contador = contador +1
            for n in range (0, int(math.ceil(float(contador)/10.0))):
                respuesta += "<a href='/" + "index.html?offset=" + str(n) + "'>" + str(n+1) + " " + "</a>"

        except Alojamiento.DoesNotExist:
            respuesta = ("No hay alojamientos disponibles, debe usted actualizar dichos alojamientos")

        # Para pasar los datos del menu de navegacion asi como el estilo de la pagina escogida
        navegacion = Menu(True)
        try:
            usuarios = ConfiguracionUsuario.objects.all()
            adicional = PagUsers(usuarios)
        except ConfiguracionUsuario.DoesNotExist:
            adicional = ""
        try:
            user = ConfiguracionUsuario.objects.get(user=request.user)
            color = user.color
            letra = user.letra
        except ConfiguracionUsuario.DoesNotExist:
            color, letra = ("", "")

    rendered = Render(request, color, letra, titulo, navegacion, respuesta, adicional)
    return HttpResponse(rendered)


# Muestra todos los alojamientos de la base de datos y permite filtrar or categorias
@csrf_exempt
def alojamientos(request):
    titulo = ("Lista de todos los alojamientos de Madrid: ")
    # Muestro el formulario de filtrado y actualizar
    form_filtrar = FormFiltrar()
    form_act = FormActualizar()
    contenido = form_filtrar + form_act

    if request.method == "GET":
        try:
            lista_alojamientos = Alojamiento.objects.all()
            contenido += "<p>"
            for alojamiento in lista_alojamientos:
                #web = unicode.encode(alojamiento.web)
                contenido += "<li>" + str(alojamiento.nombre) + ": " + "<a href='/" + \
                            str(alojamiento.web) + "'>" + str(alojamiento.web) + "</a>"
            contenido += '</p>'
        except Alojamiento.DoesNotExist:
            contenido = ("No hay alojamientos disponibles, debe usted actualizar dichos alojamientos")

    # Si se ha filtrado o actualizado
    elif request.method == "POST":
        contenido = form_filtrar + form_act
        # Filtro los alojamientos
        if request.POST.get("tipo") == "Filtrar":
            alojamientos, num = FiltrarAlojamientos(request)   # Filtro alojamientos
            contenido += ImprimirAloj(request, alojamientos, num)  # Imprimo los alojamientos
        # Guardo los alojamientos
        elif request.POST.get("tipo") == "actualizar":
            lista_alojamientos = xml_parser.parse(1) # Por defecto, 1 es español, 2 es inglés y 3 es francés
            for alojamiento in lista_alojamientos:
                direc = alojamiento['address'] + '. ' + alojamiento['zipcode'] + '. ' + \
                        alojamiento['subAdministrativeArea'] + '. (' + alojamiento['latitude'] + ', ' + \
                        alojamiento['longitude'] + '). ' + alojamiento['country'] + '.'

                alojamiento_nuevo = Alojamiento(nombre=alojamiento['name'], email=alojamiento['email'],
                                        telefono=alojamiento['phone'], descripcion=alojamiento['body'],
                                        web=alojamiento['web'], direccion=direc,
                                        categoria=alojamiento['Categoria'], subcategoria=alojamiento['SubCategoria'])
                alojamiento_nuevo.save()
                # Guardo 5 imagenes
                imagen1, imagen2, imagen3, imagen4, imagen5 = ('', '', '', '', '')
                try:
                    imagenes = alojamiento['imagenes']
                    imagen1 = imagenes.split(' , ')[0]
                    imagen2 = imagenes.split(' , ')[1]
                    imagen3 = imagenes.split(' , ')[2]
                    imagen4 = imagenes.split(' , ')[3]
                    imagen5 = imagenes.split(' , ')[4]
                except IndexError:
                    None

                imagenes_nuevas = Imagenes(alojamiento=alojamiento['name'], url1=imagen1,
                                    url2=imagen2, url3=imagen3, url4=imagen4, url5=imagen5)
                imagenes_nuevas.save()

            return HttpResponseRedirect('/alojamientos') # Actualizo la lista de alojamientos

    else:
        contenido = "ERROR"

    # Para pasar los datos del menu de navegacion asi como el estilo de la pagina escogida
    navegacion = Menu(False)
    try:
        usuarios = ConfiguracionUsuario.objects.all()
        adicional = PagUsers(usuarios)
    except ConfiguracionUsuario.DoesNotExist:
        adicional = ""
    try:
        user = ConfiguracionUsuario.objects.get(user=request.user)
        color = user.color
        letra = user.letra
    except ConfiguracionUsuario.DoesNotExist:
        color, letra = ("", "")
    rendered = Render(request, color, letra, titulo, navegacion, contenido, adicional)
    return HttpResponse(rendered)


# Muestra la informacion de un alojamiento concreto
@csrf_exempt
def aloj_id(request, id):
    form_coment = FormComent(request.user.username, id)
    form_idioma = FormIdioma(id)
    respuesta = ''
    try:
        alojamiento = Alojamiento.objects.get(id=id)
        titulo = alojamiento.nombre
        imagenes = Imagenes.objects.get(alojamiento=alojamiento.nombre)
        comentarios = Comentario.objects.all()
        # Muestro todas las imagenes
        if unicode.encode(imagenes.url1) != "":
            respuesta = '<br>' + '<img src="' + imagenes.url1 + '"width="400" height="300" border="7">'
        if unicode.encode(imagenes.url2) != "":
            respuesta += '<br>' + '<img src="' + imagenes.url2 + '"width="400" height="300" border="7">'
        if unicode.encode(imagenes.url3) != "":
            respuesta += '<br>' + '<img src="' + imagenes.url3 + '"width="400" height="300" border="7">'
        if unicode.encode(imagenes.url4) != "":
            respuesta += '<br>' + '<img src="' + imagenes.url4 + '"width="400" height="300" border="7">'
        if unicode.encode(imagenes.url5) != "":
            respuesta += '<br>' + '<img src="' + imagenes.url5 + '"width="400" height="300" border="7">'
    except Alojamiento.DoesNotExist:
        contenido = ("No se encuentra dicho alojamienta")
    except Imagenes.DoesNotExist:
        None
    # Al ser visitado el alojamiento, aumento en 1 el numero de visitas que tiene
    if request.method == "GET":
        num_visitas = alojamiento.num_visitas+1
        guardar_alojamiento = Alojamiento(id= id, nombre=alojamiento.nombre, email=alojamiento.email,
                                        telefono=alojamiento.telefono, descripcion=alojamiento.descripcion,
                                        web=alojamiento.web, direccion=alojamiento.direccion,
                                        categoria=alojamiento.categoria, subcategoria=alojamiento.subcategoria,
                                        num_visitas=num_visitas, num_comentarios=alojamiento.num_comentarios)
        guardar_alojamiento.save()
        # Muestro toda la informacion del hotel
        contenido = alojamiento.descripcion + \
                    alojamiento.direccion + '</br>' + \
                    '<br>' + str(alojamiento.telefono) + '</br>' + "<a href='" + \
                    str(alojamiento.web) + "'>" + str(alojamiento.web) + "</a>"
        # Añado imagenes a la respuesta y el formulario del idioma
        contenido += respuesta + form_idioma
        alojamiento = Alojamiento.objects.get(id=id)
        if request.user.is_authenticated():
            contenido += FormEscogerAloj()
        contenido += '<br>' + str(num_visitas) + " visitas" + "<br><br>Comentarios: </br>"
        # Muestro comentarios
        for comentario in comentarios:
            if int(comentario.alojamiento_id) == int(id):
                contenido += '<br>' + str(comentario.fecha) + ": " + str(comentario.contenido) + '</br>'
        if request.user.is_authenticated():
            contenido += form_coment

    elif request.method == "POST":
        alojamiento = Alojamiento.objects.get(id=id)
        # Almaceno elcomentario recibido
        if request.POST.get("tipo") == "comentario":
            coment = request.POST.get("mensaje")
            fecha = str(datetime.now())
            fecha = fecha.split('.')[0]
            usuario = request.user.username
            num_comentarios = alojamiento.num_comentarios + 1
            guardar_alojamiento = Alojamiento(id= id, nombre=alojamiento.nombre, email=alojamiento.email,
                                            telefono=alojamiento.telefono, descripcion=alojamiento.descripcion,
                                            web=alojamiento.web, direccion=alojamiento.direccion,
                                            categoria=alojamiento.categoria, subcategoria=alojamiento.subcategoria,
                                            num_visitas=alojamiento.num_visitas, num_comentarios=num_comentarios)
            guardar_alojamiento.save()
            comentario_nuevo = Comentario(contenido=coment, fecha=fecha,
                                        user=usuario, alojamiento_id=id)
            comentario_nuevo.save()

            contenido = "Comentario realizado correctamente" + \
                        '<meta http-equiv="refresh" content="2;url=' '" />'
        # Almaceno el alojamiento en la pagina del usuario que lo ha escogido
        elif request.POST.get("tipo") == "escoger":
            user = request.user.username
            aloj_id = id
            fecha = str(datetime.now())
            fecha = fecha.split('.')[0]
            try:
                AlojamientoEscogido.objects.get(alojamiento_id=id)
                contenido = "Ya habias seleccionado este alojamiento" + \
                            '<meta http-equiv="refresh" content="1;url=' '" />'
            except AlojamientoEscogido.DoesNotExist:
                escogido_nuevo = AlojamientoEscogido(user=user, alojamiento_id=id, fecha_eleccion=fecha)
                escogido_nuevo.save()
                contenido = "Alojamiento escogido correctamente" + \
                            '<meta http-equiv="refresh" content="1;url=' '" />'
        # Para mostrar la informacion en otro idioma
        elif request.POST.get("tipo") == "idioma":
            idioma =  request.POST.get("Idioma")
            alojamiento = Alojamiento.objects.get(id=id)
            nombre = alojamiento.nombre
            (nombre, direc, email, telefono, descripcion, web) = EnOtroIdioma(nombre, int(idioma))
            if nombre != "error":  # Si el nombre es error es porque la informacion no esta en frances
                contenido = descripcion + direc + '</br>' + \
                            '<br>' + str(telefono) + '</br>' + "<a href='" + \
                            str(web) + "'>" + str(web) + "</a>"
            else:
                contenido = "<h4>No se dispone de la informacion de este alojamiento en frances</h4>"
            # Muestro comentarios.  Si esta logueado, form para comentar y escoger
            contenido += respuesta + form_idioma
            if request.user.is_authenticated():
                contenido += FormEscogerAloj()
            contenido += '<br>' + str(alojamiento.num_visitas) + " visitas" + "<br><br>Comentarios: </br>"
            for comentario in comentarios:
                if int(comentario.alojamiento_id) == int(id):
                    contenido += '<br>' + str(comentario.fecha) + ": " + str(comentario.contenido) + '</br>'
            if request.user.is_authenticated():
                contenido += form_coment

        else:
            contenido = "Ha ocurrido un error"
    else:
        contenido = "Metodo no permitido"

    navegacion = Menu(False)
    try:
        usuarios = ConfiguracionUsuario.objects.all()
        adicional = PagUsers(usuarios)
    except ConfiguracionUsuario.DoesNotExist:
        adicional = ""
    color, letra = ("b", 12)
    try:
        user = ConfiguracionUsuario.objects.get(user=request.user)
        color = user.color
        letra = user.letra
    except ConfiguracionUsuario.DoesNotExist:
        None
    rendered = Render(request, color, letra, titulo, navegacion, contenido, adicional)
    return HttpResponse(rendered)


# Informacion del about
def about(request):
    titulo = "Informacion sobre la pagina web"
    contenido = info_about()
    navegacion = Menu(False)
    try:
        usuarios = ConfiguracionUsuario.objects.all()
        adicional = PagUsers(usuarios)
    except ConfiguracionUsuario.DoesNotExist:
        adicional = ""
    try:
        user = ConfiguracionUsuario.objects.get(user=request.user)
        color = user.color
        letra = user.letra
    except ConfiguracionUsuario.DoesNotExist:
        color, letra = ("", "")
    rendered = Render(request, color, letra, titulo, navegacion, contenido, adicional)
    return HttpResponse(rendered)


# Perfil en xml
def profile_xml(request, user):
    if request.method == "GET":
        escogidos = AlojamientoEscogido.objects.filter(user=user)
        contenido = '<?xml version="1.0" encoding="UTF-8"?>\n'
        contenido += '<serviceList>Canal XML de \n\t' + user
        for escogido in escogidos:
            alojamiento = Alojamiento.objects.get(id=escogido.alojamiento_id)
            imagenes = Imagenes.objects.get(alojamiento=alojamiento.nombre)
            imagen = imagenes.url1
            nombre = alojamiento.nombre
            descripcion = alojamiento.descripcion
            direccion = alojamiento.direccion
            web = alojamiento.web
            categoria = alojamiento.categoria
            subcategoria = alojamiento.subcategoria
            contenido += '<service>'
            contenido += '\t<basicData>'
            contenido += '\t\t<name><![CDATA[ ' + nombre + '\t\t ]]></name>'
            contenido += '\t\t<web>' + web + '\t\t</web>'
            contenido += '\t\t<body><![CDATA[ ' + descripcion + '\t\t ]]></body>'
            contenido += '\t</basicData>'
            contenido += '\t<geoData>'
            contenido += '\t\t<address>' + direccion + '\t\t</address>'
            contenido += '\t</geoData>'
            contenido += '\t<multimedia>' + '\t\t<media type="image">'
            contenido += '\t\t<url>' + imagen + '\t\t</url>'
            contenido += '\t\t</media>' + '\t</multimedia>'
            contenido += '\t<extradata>' + '\t\t<categoria>'
            contenido += '\t\t<item name="Categoria">' + categoria + '\t\t</item>' + '\t\t\t<subcategoria>'
            contenido += '\t\t\t<item name="SubCategoria">' + subcategoria + '\t\t\t</item>'
            contenido += '\t\t\t</subcategoria>' + '\t\t</categoria>' + '\t</extradata>'
            contenido += '</service>'

        contenido += '</serviceList>\n'
        return HttpResponse(contenido, content_type="text/xml")

    else:
        return HttpResponseNotFound('Metodo no valido')
