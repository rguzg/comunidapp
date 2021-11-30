from .models import Autor, Editorial, Pais, Relaciones_Profesores, Revista, User, LineaInvestigacion, Facultad, Nivel, PalabrasClave, Articulo, CapituloLibro, Patente, Congreso, Investigacion, Tesis
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

    class FacultadField(Field):
        # Esta función agrega a value la instancia del modelo que se esté serializando
        def get_attribute(self, instance):
            return instance

        # Value almacena los atributos del modelo que esté serializando el serializer
        def to_representation(self, value):
                facultades = []
                if(value.user):
                    for facultad in value.user.facultades.all():
                        facultades.append(Facultad_Serializer(facultad).data)

                return facultades

    class ClaveField(Field):
        # Esta función agrega a value la instancia del modelo que se esté serializando
        def get_attribute(self, instance):
            return instance

        # Value almacena los atributos del modelo que esté serializando el serializer
        def to_representation(self, value):
                if(value.user):
                    return value.user.clave
                else:
                    return None
   
    class LineasInvestigacionField(Field):
        # Esta función agrega a value la instancia del modelo que se esté serializando
        def get_attribute(self, instance):
            return instance

        # Value almacena los atributos del modelo que esté serializando el serializer
        def to_representation(self, value):
                investigaciones = []
                if(value.user):
                    for investigacion in value.user.investigaciones.all():
                        investigaciones.append(LineasInvestigacion_Serializer(investigacion).data)

                return investigaciones

    first_name = FirstNameField()
    last_name = LastNameField()
    facultad = FacultadField()
    clave = ClaveField()
    lineas_investigacion = LineasInvestigacionField()

    class Meta:
        model = Autor
        fields = ['id', 'first_name', 'last_name', 'facultad', 'clave', 'lineas_investigacion', 'user'] 
        read_only_fields = ['id', 'first_name', 'last_name', 'facultad', 'clave', 'lineas_investigacion', 'user'] 

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

class Pais_Serializer(ModelSerializer):
    class Meta:
        model = Pais
        fields = '__all__'

class Revista_Serializer(ModelSerializer):
    class Meta:
        model = Revista
        fields = '__all__'


class Editorial_Serializer(ModelSerializer):
    class Meta:
        model = Editorial
        fields = '__all__'
class Articulo_Serializer(ModelSerializer):

    primer_colaborador = Autor_Serializer(read_only=True)
    segundo_colaborador = Autor_Serializer(read_only=True)
    tercer_colaborador = Autor_Serializer(read_only=True)
    cuarto_colaborador = Autor_Serializer(read_only=True)
    palabras_clave = PalabrasClave_Serializer(read_only=True, many=True)
    pais = Pais_Serializer(read_only=True)
    revista = Revista_Serializer(read_only=True)
    editorial = Editorial_Serializer(read_only=True)
    lineas_investigacion = LineasInvestigacion_Serializer(
        read_only=True, many=True)
    class Meta:
        model = Articulo
        fields = '__all__'


class CapituloLibro_Serializer(ModelSerializer):
    primer_autor = Autor_Serializer(read_only=True)
    primer_coautor = Autor_Serializer(read_only=True)
    segundo_coautor = Autor_Serializer(read_only=True)
    tercer_coautor = Autor_Serializer(read_only=True)
    cuarto_coautor = Autor_Serializer(read_only=True)
    palabras_clave = PalabrasClave_Serializer(read_only=True, many=True)
    pais = Pais_Serializer(read_only=True)
    editorial = Editorial_Serializer(read_only=True)
    lineas_investigacion = LineasInvestigacion_Serializer(
        read_only=True, many=True)

    class Meta:
        model = CapituloLibro
        fields = '__all__'


class Patente_Serializer(ModelSerializer):
    pais = Pais_Serializer(read_only=True)
    lineas_investigacion = LineasInvestigacion_Serializer(
        read_only=True, many=True)
    class Meta:
        model = Patente
        fields = '__all__'


class Congreso_Serializer(ModelSerializer):
    primer_autor = Autor_Serializer(read_only=True)
    primer_colaborador = Autor_Serializer(read_only=True)
    segundo_colaborador = Autor_Serializer(read_only=True)
    tercer_colaborador = Autor_Serializer(read_only=True)
    cuarto_colaborador = Autor_Serializer(read_only=True)
    palabras_clave = PalabrasClave_Serializer(read_only=True, many=True)
    pais = Pais_Serializer(read_only=True)
    estadoP = Estado_Serializer(read_only=True)
    ciudad = Ciudad_Serializer(read_only=True)
    editorial = Editorial_Serializer(read_only=True)
    lineas_investigacion = LineasInvestigacion_Serializer(
        read_only=True, many=True)
    palabras_clave = PalabrasClave_Serializer(
        read_only=True, many=True)

    class Meta:
        model = Congreso
        fields = '__all__'

class Investigacion_Serializer(ModelSerializer):

    responsable = Autor_Serializer(read_only=True)
    primer_colaborador = Autor_Serializer(read_only=True)
    segundo_colaborador = Autor_Serializer(read_only=True)
    primer_alumno = Alumno_Serializer(read_only=True)
    segundo_alumno = Alumno_Serializer(read_only=True)
    tercer_alumno = Alumno_Serializer(read_only=True)
    palabras_clave = PalabrasClave_Serializer(read_only=True, many=True)
    lineas_investigacion = LineasInvestigacion_Serializer(
        read_only=True, many=True)
    institucion = Institucion_Serializer(read_only=True, many=True)

    class Meta:
        model = Investigacion
        fields = '__all__'


class Tesis_Serializer(ModelSerializer):

    alumno = Alumno_Serializer(read_only=True)
    primer_colaborador = Autor_Serializer(read_only=True)
    segundo_colaborador = Autor_Serializer(read_only=True)
    tercer_colaborador = Autor_Serializer(read_only=True)
    cuarto_colaborador = Autor_Serializer(read_only=True)
    palabras_clave = PalabrasClave_Serializer(read_only=True, many=True)
    lineas_investigacion = LineasInvestigacion_Serializer(
        read_only=True, many=True)
    institucion = Institucion_Serializer(read_only=True, many=True)
    profesor = User_Serializer(read_only=True)

    class Meta:
        model = Tesis
        fields = '__all__'
