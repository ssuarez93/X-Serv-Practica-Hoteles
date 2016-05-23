
#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from models import Alojamiento
import sys
import string
import urllib , urllib2
import os.path


def normalize_whitespace(text):
    "Remove redundant whitespace from a string"
    return string.join(string.split(text), ' ')

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.theContent = ''
        self.inContent = False
        self.inItem = False
        self.inCategoria = False
        self.inSubcategoria = False
        self.imagenes = ''
        self.lista_alojamientos = []
        self.dicc_alojamientos = {'name': "", 'email': '', 'phone': '', 'body': '',
                                'web': "", 'address': '', 'zipcode': '', 'country': '',
                                'latitude': '', 'longitude': '', 'subAdministrativeArea': '',
                                'Categoria': "", 'SubCategoria': "", 'imagenes': ''}


    def startElement (self, name, attrs):
        if name in ['name', 'email', 'phone', 'body', 'web',
                    'address', 'zipcode', 'country', 'latitude',
                    'longitude', 'subAdministrativeArea']:
            self.inItem = True
            self.inContent = True

        if name == 'media' and attrs["type"] == "image":
            self.inItem = True
        elif self.inItem:
            if name == "url":
                self.inContent = True

        if name == 'item':
            if attrs["name"] == "Categoria":
                self.inItem = True
                self.inContent = True
                self.inCategoria = True
            elif attrs["name"] == "SubCategoria":
                self.inItem = True
                self.inContent = True
                self.inSubcategoria = True


    def endElement (self, name):
        if name in ['name', 'email', 'phone', 'body', 'web',
                    'address', 'zipcode', 'country', 'latitude',
                    'longitude', 'subAdministrativeArea']:
            self.dicc_alojamientos[name] = self.theContent
            self.inItem = False
            self.inContent = False
            self.theContent = ""

        if name == "media":
            self.inItem = False
        elif self.inItem :
            if name == "url" :
                self.imagenes += self.theContent + " , "
                self.inContent = False
                self.theContent = ""

        if name in ['item']:
            if self.inCategoria:
                self.dicc_alojamientos['Categoria'] = self.theContent
                self.inItem = False
                self.inContent = False
                self.inCategoria = False
                self.theContent = ""
            if self.inSubcategoria:
                self.dicc_alojamientos['SubCategoria'] = self.theContent
                self.inItem = False
                self.inContent = False
                self.inSubcategoria = False
                self.theContent = ""

        if name == "service":
            self.dicc_alojamientos['imagenes'] = self.imagenes
            self.imagenes = ''
            self.lista_alojamientos.append(self.dicc_alojamientos)
            self.dicc_alojamientos = {'name': "", 'email': '', 'phone': '', 'body': '',
                                    'web': "", 'address': '', 'zipcode': '', 'country': '',
                                    'latitude': '', 'longitude': '', 'subAdministrativeArea': '',
                                    'Categoria': "", 'SubCategoria': "", 'imagenes': ''}


    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

def parse(index):
# Ready, set, go!
    xml_language = {1: 'es', 2: 'en', 3: 'fr'}
    xmlURL = 'http://cursosweb.github.io/etc/alojamientos_' + str(xml_language[index]) + '.xml'
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    theParser.parse(xmlURL)
    return theHandler.lista_alojamientos
