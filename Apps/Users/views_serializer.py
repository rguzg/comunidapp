from .serializers import Facultad_Serializer, LineasInvestigacion_Serializer, Nivel_Serializer, PalabrasClave_Serializer
from rest_framework import generics, permissions
from .models import PalabrasClave

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

