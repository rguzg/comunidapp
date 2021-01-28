from .models import Facultad, LineaInvestigacion, Nivel, PalabrasClave
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

class BuscarFacultades(View):
    def get(self, request):
        try:
            queryResult = Facultad.objects.filter(Q(nombre__icontains = request.GET['q']))

            json = {
                'status': 200,
                'mensaje': []
            }

            for facultad in queryResult:
                json['mensaje'].append(facultad.nombre)

            return JsonResponse(json)
        except:
            return JsonResponse({'status': 400, 'mensaje': "El query parameter 'q' es obligatorio"})

class BuscarNiveles(View):
    def get(self, request):
        try:
            queryResult = Nivel.objects.filter(Q(nombre__icontains = request.GET['q']))

            json = {
                'status': 200,
                'mensaje': []
            }

            for nivel in queryResult:
                json['mensaje'].append(nivel.nombre)

            return JsonResponse(json)
        except:
            return JsonResponse({'status': 400, 'mensaje': "El query parameter 'q' es obligatorio"})


