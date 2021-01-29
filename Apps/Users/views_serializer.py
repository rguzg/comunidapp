from .models import LineaInvestigacion
from .serializers import LineasInvestigacion_Serializer
from rest_framework import generics, permissions

class LineasInvestigacion_Serializer_View(generics.ListCreateAPIView):
    serializer_class = LineasInvestigacion_Serializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.investigaciones.all()