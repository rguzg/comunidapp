from .models import (Articulo, CapituloLibro, Patente, Congreso, Investigacion, Tesis,  Contrato, Facultad, LineaInvestigacion, Nivel, Pais, User, UpdateRequest, Autor)
from django.views import View
from django.db.models import Q, query 
from django.http.response import JsonResponse


class BuscarLineas(View):
    def get(self, request):
        try:
            queryResult = LineaInvestigacion.objects.filter(Q(nombre__icontains = request.GET['q']))

            json = {
                'status': 200,
                'mensaje': []
            }

            for linea in queryResult:
                json['mensaje'].append(linea.nombre)

            return JsonResponse(json)
        except:
            return JsonResponse({'status': 400, 'mensaje': "El query parameter 'q' es obligatorio"})
