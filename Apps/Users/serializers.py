from .models import Autor, Relaciones_Profesores, User, LineaInvestigacion, Facultad, Nivel, PalabrasClave
from rest_framework import serializers
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

# Este serializer estaba siendo utilizado para los JSON para los grafos, pero fue descontinuado a favor del serializador de autores ya que no todos los autores tienen usuarios
class Users_Serializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username'] 
        read_only_fields = ['id', 'first_name', 'last_name', 'username'] 

class Autor_Serializer(ModelSerializer):
    class Meta:
        model = Autor
        fields = ['id', 'first_name', 'last_name', 'user'] 
        read_only_fields = ['id', 'first_name', 'last_name', 'user'] 

class Relaciones_Serializer(ModelSerializer):
    source = serializers.IntegerField(source = 'profesor1.pk')
    target = serializers.IntegerField(source = 'profesor2.pk', allow_null = True)
    
    class Meta:
        model = Relaciones_Profesores
        fields = ['source', 'target']
        read_only_fields = ['source', 'target']
