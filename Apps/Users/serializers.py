from .models import Autor, Relaciones_Profesores, User, LineaInvestigacion, Facultad, Nivel, PalabrasClave
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Field, Serializer

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
    # Explicando estos dos fields: No todos los autores tienen los nombres colocados en los campos 
    # first_name y last_name del modelo. Afortunadamente algunos autores están relacionados con algun User
    # y si los nombres están ahí, se extraen de ahí. Si no están se utiliza el username del autor.

    # Además de eso, no se utilizaron defaults para generar los nombres porque para que funcione un default es necesario
    # que el campo no exista en la instancia del modelo y eso no ocurre con los datos que estamos procesando
    
    # No se agregaró el método to_internal_value porqué first_name y last_name son read-only fields

    class FirstNameField(Field):
        def get_attribute(self, instance):
            # Esta función agrega a value la instancia del modelo que se esté serializando
            return instance


        # Value almacena los atributos del modelo que esté serializando el serializer        
        def to_representation(self, value):
            if(value.first_name):
                return value.first_name
            else:
                first_name = ""

                if(value.user):
                    if(value.user.first_name):
                        first_name += value.user.first_name
                    else:
                        first_name += value.user.username

                return first_name

    class LastNameField(Field):
        # Esta función agrega a value la instancia del modelo que se esté serializando
        def get_attribute(self, instance):
            return instance

        # Value almacena los atributos del modelo que esté serializando el serializer
        def to_representation(self, value):
            if(value.last_name):
                return value.last_name
            else:
                if(value.user):
                    if(value.user.last_name):
                       return value.user.last_name

    first_name = FirstNameField()
    last_name = LastNameField()

    class Meta:
        model = Autor
        fields = ['id', 'first_name', 'last_name', 'user'] 
        read_only_fields = ['id', 'first_name', 'last_name', 'user'] 

class Relaciones_Serializer(ModelSerializer):

    # A la API que genera los grafos en el front no le gusta que target sea null, entonces si en la instancia del modelo profesor2 es None, el 
    # valor serializado se convierte en el valor de profesor1
    class TargetField(Field):
        # Esta función agrega a value la instancia del modelo que se esté serializando
        def get_attribute(self, instance):
            return instance

        # Value almacena los atributos del modelo que esté serializando el serializer
        def to_representation(self, value):
            if(value.profesor2):
                return value.profesor2.pk
            else:
                return value.profesor1.pk

    source = serializers.IntegerField(source = 'profesor1.pk')
    target = TargetField()
    
    class Meta:
        model = Relaciones_Profesores
        fields = ['source', 'target']
        read_only_fields = ['source', 'target']
