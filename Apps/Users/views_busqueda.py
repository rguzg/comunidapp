from .models import Facultad, LineaInvestigacion, Nivel, PalabrasClave
from django.views import View
from django.db.models import Q 
from django.http.response import JsonResponse


class BuscarLineas(View):
    def get(self, request):
        try:
            queryResult = LineaInvestigacion.objects.filter(Q(nombre__icontains = request.GET['q']))

            json = {
                'mensaje': []
            }

            for linea in queryResult:
                json['mensaje'].append({'id': linea.id, 'nombre': linea.nombre})

            return JsonResponse(json)
        except:
            return JsonResponse({'status': 400, 'mensaje': "El query parameter 'q' es obligatorio"})

class BuscarFacultades(View):
    def get(self, request):
        try:
            queryResult = Facultad.objects.filter(Q(nombre__icontains = request.GET['q']))

            json = {
                'mensaje': []
            }

            for facultad in queryResult:
                json['mensaje'].append({'id': facultad.id, 'nombre': facultad.nombre})

            return JsonResponse(json)
        except:
            return JsonResponse({'status': 400, 'mensaje': "El query parameter 'q' es obligatorio"})

class BuscarNiveles(View):
    def get(self, request):
        try:
            queryResult = Nivel.objects.filter(Q(nombre__icontains = request.GET['q']))

            json = {
                'mensaje': []
            }

            for nivel in queryResult:
                json['mensaje'].append({'id': nivel.id, 'nombre': nivel.nombre})

            return JsonResponse(json)
        except:
            return JsonResponse({'status': 400, 'mensaje': "El query parameter 'q' es obligatorio"})

class BuscarPalabrasClave(View):
    def get(self, request):
        try:
            queryResult = PalabrasClave.objects.filter(Q(nombre__icontains = request.GET['q']))

            json = {
                'mensaje': []
            }

            for palabra in queryResult:
                json['mensaje'].append({'id': palabra.id, 'nombre': palabra.nombre})

            return JsonResponse(json)
        except:
            return JsonResponse({'status': 400, 'mensaje': "El query parameter 'q' es obligatorio"})
