# Las views de Django que procesan forms directamente requieren que el body de la petición tengan un 
# patrón muy especifico. Estas views procesan la petición que incluye las cosas que se pusieron en el input_pill 
# y después crea otra petición que sea compatible con la que utilizan las forms

from typing import Any
from django.http.response import HttpResponse
from django.views import View
from django.db import models
from .models import Facultad, LineaInvestigacion, Nivel
import ast
import requests

class Proxy(View):
    def post(self, request):
        request_body = {
            'investigaciones': [],
            'niveles': [],
            'facultades': []
        }

        files = []

        if(request.POST['lineas']):
            lineas = ast.literal_eval(request.POST['lineas'])
            if(type(lineas) == dict):
                request_body['investigaciones'].append(self.ObtenerIDObjeto(LineaInvestigacion, lineas['nombre']))
            elif(type(lineas) == tuple):
                for linea in lineas:
                    request_body['investigaciones'].append(self.ObtenerIDObjeto(LineaInvestigacion, linea['nombre']))
        if(request.POST['niveles']):
            niveles = ast.literal_eval(request.POST['niveles'])
            if(type(niveles) == dict):
                request_body['niveles'].append(self.ObtenerIDObjeto(Nivel, niveles['nombre']))
            elif(type(niveles) == tuple):
                for nivel in niveles:
                    request_body['niveles'].append(self.ObtenerIDObjeto(Nivel, nivel['nombre']))
        if(request.POST['facultades']):
            facultades = ast.literal_eval(request.POST['facultades'])
            if(type(facultades) == dict):
                request_body['facultades'].append(self.ObtenerIDObjeto(Facultad, facultades['nombre']))
            elif(type(facultades) == tuple):
                for facultad in facultades:
                    request_body['facultades'].append(self.ObtenerIDObjeto(Facultad, facultad['nombre']))
                    
        for key in request.POST:
            if(not (key in ['lineas', 'niveles', 'facultades', 'csrfmiddlewaretoken'])):
                request_body[key] = request.POST[key]
        
        for key in request.FILES:
            files.append((key, (request.FILES[key].name, request.FILES[key].read(), request.FILES[key].content_type)))

        csrf_token = requests.get('http://localhost:8000/profile').cookies['csrftoken']
        request_body['csrfmiddlewaretoken'] = csrf_token

        r = requests.post('http://localhost:8000/profile', request_body, cookies = {
            'csrftoken': csrf_token,
            'sessionid': request.COOKIES['sessionid'],
        }, headers = {'connection': 'close'}, files = files)

        return HttpResponse(200)

    def ObtenerIDObjeto(self, modelo: Any, nombre_objeto: str) -> int:
        objeto = modelo.objects.filter(models.Q(nombre__exact = nombre_objeto)).first()
        if(not objeto):
            nuevoObjeto = modelo(nombre = nombre_objeto)
            nuevoObjeto.save()

            return nuevoObjeto.id
        else:
            return objeto.id


