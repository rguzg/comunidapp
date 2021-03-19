from .models import LineaInvestigacion, Facultad, Nivel, PalabrasClave
from rest_framework.serializers import ModelSerializer

class LineasInvestigacion_Serializer(ModelSerializer):
    class Meta:
        model = LineaInvestigacion
        fields = '__all__'

class Facultad_Serializer(ModelSerializer):
    class Meta:
        model = Facultad
        fields = '__all__'

class Nivel_Serializer(ModelSerializer):
    class Meta:
        model = Nivel
        fields = '__all__'

class PalabrasClave_Serializer(ModelSerializer):
    class Meta:
        model = PalabrasClave
        fields = '__all__'
