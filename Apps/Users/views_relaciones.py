from rest_framework import authentication, permissions
from rest_framework.views import APIView, exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Articulo, Relaciones_Profesores
from .serializers import Autor_Serializer, Users_Serializer, Relaciones_Serializer
from django.views import View
from django.shortcuts import HttpResponse, redirect, render
from django.db.models import Q

class Relaciones(APIView):
    authentication_classes = [authentication.SessionAuthentication]

    def get(self, request, producto):
        producto = producto.lower()
        relaciones = None
        switch_productos = None
        
        try:
            show_alumnos = True if request.query_params['alumnos'] == 'true' else False
        # En caso de que no se mande el query_params
        except KeyError:
            show_alumnos = False

            switch_productos = {
                "articulos": lambda : Relaciones_Profesores.objects.exclude(articulo = None),
                "capituloslibros": lambda : Relaciones_Profesores.objects.exclude(capituloLibro = None),
                "patentes": lambda :  Relaciones_Profesores.objects.exclude(patente = None),
                "congresos": lambda :  Relaciones_Profesores.objects.exclude(congreso = None),
                "investigaciones": lambda :  Relaciones_Profesores.objects.exclude(investigacion = None),
                "tesis": lambda :  Relaciones_Profesores.objects.exclude(tesis = None),
            }

        resultado = {
            'nodes': [],
            'edges': []
        }

        try:
            if(show_alumnos):
                relaciones = switch_productos[producto]()
            else:
                relaciones = switch_productos[producto]().filter(profesor1__alumno = False, profesor2__alumno = False)
        except KeyError as e:
            raise NotFound(f'{e} no es un producto valido', 404)
        
        for relacion in relaciones:
            profesor1 = Autor_Serializer(relacion.profesor1).data
            if(profesor1 not in resultado['nodes']):
                resultado['nodes'].append(profesor1)
            if(relacion.profesor2):
                profesor2 = Autor_Serializer(relacion.profesor2).data
                if(profesor2 not in resultado['nodes']):
                    resultado['nodes'].append(profesor2)

            relacion_serializada = Relaciones_Serializer(relacion).data

            resultado['edges'].append(relacion_serializada)
        return Response(resultado)

class Visualization(View):
    def get(self, request):
        return render(request, 'visualization.html')

class VisualizationFull(View):
    def get(self, request):
        return render(request, 'visualization-full.html')