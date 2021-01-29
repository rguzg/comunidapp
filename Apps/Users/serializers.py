from .models import LineaInvestigacion
from rest_framework.serializers import ModelSerializer

class LineasInvestigacion_Serializer(ModelSerializer):
    class Meta:
        model = LineaInvestigacion
        exclude = ['id']
