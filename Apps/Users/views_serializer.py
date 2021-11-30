from .serializers import Facultad_Serializer, LineasInvestigacion_Serializer, Nivel_Serializer, PalabrasClave_Serializer, Articulo_Serializer, CapituloLibro_Serializer, Patente_Serializer, Congreso_Serializer, Investigacion_Serializer, Tesis_Serializer
from rest_framework import generics, permissions
from drf_multiple_model.views import ObjectMultipleModelAPIView
from .models import PalabrasClave, Articulo, CapituloLibro, Patente, Congreso, Investigacion, Tesis

class LineasInvestigacion_Serializer_View(generics.ListCreateAPIView):
    serializer_class = LineasInvestigacion_Serializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.investigaciones.all()

class Facultad_Serializer_View(generics.ListCreateAPIView):
    serializer_class = Facultad_Serializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.facultades.all()

class Nivel_Serializer_View(generics.ListCreateAPIView):
    serializer_class = Nivel_Serializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.niveles.all()

class PalabraClave_Serializer_View(generics.ListCreateAPIView):
    serializer_class = PalabrasClave_Serializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = PalabrasClave.objects.all()


class Productos_Serializer_View(ObjectMultipleModelAPIView):
    permission_classes = [permissions.IsAuthenticated]
    querylist = [
        {'queryset': Articulo.objects.all(), 'serializer_class': Articulo_Serializer},
        {'queryset': CapituloLibro.objects.all(
        ), 'serializer_class': CapituloLibro_Serializer},
        {'queryset': Patente.objects.all(), 'serializer_class': Patente_Serializer},
        {'queryset': Congreso.objects.all(), 'serializer_class': Congreso_Serializer},
        {'queryset': Investigacion.objects.all(
        ), 'serializer_class': Investigacion_Serializer},
        {'queryset': Tesis.objects.all(), 'serializer_class': Tesis_Serializer},
    ]
