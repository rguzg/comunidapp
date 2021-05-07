from rest_framework import authentication, permissions
from rest_framework.views import APIView, exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Articulo, Relaciones_Profesores
from .serializers import Users_Serializer, Relaciones_Serializer
from django.views import View
from django.shortcuts import HttpResponse, redirect, render


class Relaciones(APIView):
    authentication_classes = [authentication.SessionAuthentication]

    def get(self, request, producto):
        producto = producto.lower()
        relaciones = None

        switch_productos = {
            "articulos": lambda : Relaciones_Profesores.objects.exclude(articulo = None),
            "capitulolibros": lambda : Relaciones_Profesores.objects.exclude(capituloLibro = None),
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
            relaciones = switch_productos[producto]()
        except KeyError as e:
            raise NotFound(f'{e} no es un producto valido', 404)
        
        for relacion in relaciones:
            profesor1 = Users_Serializer(relacion.profesor1.user).data
            if(profesor1 not in resultado['nodes']):
                resultado['nodes'].append(profesor1)
            if(relacion.profesor2):
                profesor2 = Users_Serializer(relacion.profesor2.user).data
                if(profesor2 not in resultado['nodes']):
                    resultado['nodes'].append(profesor2)

                resultado['edges'].append(Relaciones_Serializer(relacion).data)
        return Response(resultado)

class Prueba(View):
    def get(self, request):
        return render(request, 'Network.html')