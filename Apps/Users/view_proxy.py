# Las views de Django que procesan forms directamente requieren que el body de la petición tengan un 
# patrón muy especifico. Estas views procesan la petición que incluye las cosas que se pusieron en el input_pill 
# y después crea otra petición que sea compatible con la que utilizan las forms

HOST = "http://localhost:8000"

from typing import Any
from django.http.response import HttpResponse
from django.views import View
from django.db import models
from .models import Facultad, LineaInvestigacion, Nivel, PalabrasClave
import ast
import requests

class Proxy(View):
    def post(self, request):
        request_body = {}

        files = []

        # Este header se utiliza para saber a que URL mandar la petición que se está procesando
        # Pathname debe venir con una diagonal al principio
        pathname = request.headers['PROXY']

        if('lineas' in request.POST):
            key = ""

            # El nombre que tiene el field de lineas de investigación depende cambia según el form al que se
            # va a mandar
            if(pathname == '/add/profesor' or pathname == '/profile'):
                key = 'investigaciones'
            else:
                key = 'lineas_investigacion'

            request_body[key] = []

            lineas = ast.literal_eval(request.POST['lineas'])
            if(type(lineas) == dict):
                request_body[key].append(self.ObtenerIDObjeto(LineaInvestigacion, lineas['nombre']))
            elif(type(lineas) == tuple):
                for linea in lineas:
                    request_body[key].append(self.ObtenerIDObjeto(LineaInvestigacion, linea['nombre']))
        if('niveles' in request.POST):
            request_body['niveles'] = []

            niveles = ast.literal_eval(request.POST['niveles'])
            if(type(niveles) == dict):
                request_body['niveles'].append(self.ObtenerIDObjeto(Nivel, niveles['nombre']))
            elif(type(niveles) == tuple):
                for nivel in niveles:
                    request_body['niveles'].append(self.ObtenerIDObjeto(Nivel, nivel['nombre']))
        if('facultades' in request.POST):
            request_body['facultades'] = []

            facultades = ast.literal_eval(request.POST['facultades'])
            if(type(facultades) == dict):
                request_body['facultades'].append(self.ObtenerIDObjeto(Facultad, facultades['nombre']))
            elif(type(facultades) == tuple):
                for facultad in facultades:
                    request_body['facultades'].append(self.ObtenerIDObjeto(Facultad, facultad['nombre']))
        if('palabras' in request.POST):
            request_body['palabras_clave'] = []

            palabras = ast.literal_eval(request.POST['palabras'])
            if(type(palabras) == dict):
                request_body['palabras_clave'].append(self.ObtenerIDObjeto(PalabrasClave, palabras['nombre']))
            elif(type(palabras) == tuple):
                for palabra in palabras:
                    request_body['palabras_clave'].append(self.ObtenerIDObjeto(PalabrasClave, palabra['nombre']))
                    
        for key in request.POST:
            if(not (key in ['lineas', 'niveles', 'facultades', 'palabras', 'csrfmiddlewaretoken'])):
                request_body[key] = request.POST[key]
        
        for key in request.FILES:
            files.append((key, (request.FILES[key].name, request.FILES[key].read(), request.FILES[key].content_type)))

        csrf_token = requests.get(f'{HOST}{pathname}').cookies['csrftoken']
        request_body['csrfmiddlewaretoken'] = csrf_token

        r = requests.post(f'{HOST}{pathname}', request_body, cookies = {
            'csrftoken': csrf_token,
            'sessionid': request.COOKIES['sessionid'],
        }, files = files)

        return HttpResponse(r.text)

    def ObtenerIDObjeto(self, modelo: Any, nombre_objeto: str) -> int:
        objeto = modelo.objects.filter(models.Q(nombre__exact = nombre_objeto)).first()
        if(not objeto):
            nuevoObjeto = modelo(nombre = nombre_objeto)
            nuevoObjeto.save()

            return nuevoObjeto.id
        else:
            return objeto.id


