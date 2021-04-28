from rest_framework import authentication, permissions
from rest_framework.views import APIView, exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Relaciones_Profesores
from .serializers import Users_Serializer, Relaciones_Serializer

class Relaciones(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, producto):
        producto = producto.lower()
        relaciones = None

        switch_productos = {
            "articulos": lambda : Relaciones_Profesores.objects.exclude(articulo = None),
            "capitulolibros": lambda : Relaciones_Profesores.objects.exclude(capituloLibro = None),
            "patentes": lambda :  Relaciones_Profesores.objects.exclude(patente = None),
            "congresos": lambda :  Relaciones_Profesores.objects.exclude(congreso = None),
            "investigaciones": lambda :  Relaciones_Profesores.objects.exclude(investigacion = None),
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
            if((profesor1 := Users_Serializer(relacion.profesor1.user).data) not in resultado['nodes']):
                resultado['nodes'].append(profesor1)
            if((profesor2 := Users_Serializer(relacion.profesor2.user).data) not in resultado['nodes']):
                resultado['nodes'].append(profesor2)

            resultado['edges'].append(Relaciones_Serializer(relacion).data)
        return Response(resultado)
