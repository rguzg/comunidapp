from .models import LineaInvestigacion, Facultad, Nivel, PalabrasClave
from rest_framework.serializers import ModelSerializer

class LineasInvestigacion_Serializer(ModelSerializer):
    class Meta:
        model = LineaInvestigacion
        exclude = ['id']

class Facultad_Serializer(ModelSerializer):
    class Meta:
        model = Facultad
        exclude = ['id']

class Nivel_Serializer(ModelSerializer):
    class Meta:
        model = Nivel
        exclude = ['id']

class PalabrasClave_Serializer(ModelSerializer):
    class Meta:
        model = PalabrasClave
        exclude = ['id']
