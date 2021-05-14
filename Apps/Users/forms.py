import uuid
from django import forms
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import UserCreationForm
from .models import (Alumno, Articulo, Autor, CapituloLibro, Congreso,
                     Contrato, Editorial, Facultad, Institucion, Investigacion,
                     LineaInvestigacion, Nivel, PalabrasClave, Patente,
                     Revista, Tesis, User, UpdateRequest)

LONGITUD_NOMBRE_AUTOR = 1
LONGITUD_APELLIDO_AUTOR = 1

"""
Formularios para creacion de usuarios: Profesores y Administradores
Son necesarios 2 diferentes formularios debido a los distintos permisos de cada usuario
"""
class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2',
                  'is_superuser', 'is_staff', 'email']
        widgets = {
            'is_superuser': forms.HiddenInput(),
            'is_staff': forms.HiddenInput(),
            'email': forms.HiddenInput()
        }
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2', 'is_superuser', 'is_staff']:
            self.fields[fieldname].help_text = None

    # El modelo de usuarios administradores es el mismo que los profesores, así que es necesario pedir
    # un email, pero el form no pide uno, así que aquí se genera un email como placeholder
    def clean_email(self):
        return f'{str(uuid.uuid4())}@{str(uuid.uuid4())}.net'


class ProfesorCreationForm(UserCreationForm):
    nacimiento= forms.DateField(input_formats=['%d-%m-%Y'], required=False)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2', 'first_name', 'last_name',
                  'clave', 'sexo', 'nacimiento', 'foto', 'facultades', 'contratacion', 'grado', 
                  'investigaciones', 'niveles', 'cuerpoAcademico', 'is_superuser', 'is_staff', 'publico']
        widgets = {
            'is_superuser': forms.HiddenInput(),
            'is_staff': forms.HiddenInput(),
            'email': forms.HiddenInput(),
            'first_name': forms.TextInput(attrs={'required':'True'}),
            'last_name': forms.TextInput(attrs={'required':'True'}),
            'username': forms.EmailInput(attrs={'required':'True'})
        }
        labels = {
            'username': 'Correo electrónico',
            'sexo': 'Género',
            'investigaciones': 'Líneas de investigación',
            'publico': '¿Perfil público?'
        }
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
            'publico': 'Si activas esta opción, cualquier usuario de la plataforma podra ver tu información de contacto y tus productos'
        }

    def clean(self):
        cleaned_data = super(ProfesorCreationForm, self).clean()
        foto = cleaned_data.get('foto')
        cleaned_data['email'] = cleaned_data['username']
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        return cleaned_data


"""
CBV para los formularios de inicio de sesion y actualizacion de datos
"""
class UpdateRequestForm(ModelForm):
    nacimiento = forms.DateField(label="Nacimiento", input_formats=['%d-%m-%Y'], required=True)
    class Meta:
        model = UpdateRequest
        fields = '__all__'
        exclude = ['estado', 'changed_fields']
        labels = {
            'first_name': 'Nombre(s)',
            'last_name': 'Apellido(s)',
            'email': 'Correo electrónico',
            'user': '',
            'motivo': ''
        }
        widgets = {
            'user': forms.HiddenInput(),
            'motivo': forms.HiddenInput(),
        }

    def clean(self):
        data = {}
        cleaned_data = super(UpdateRequestForm, self).clean()
        user = cleaned_data.get('user')

        peticion = UpdateRequest.objects.filter(user=user)
        if peticion.count()>0:
            peticion = peticion.first()
            if peticion.estado == 'P' :
                self.add_error(
                    None, 
                    'Ya cuentas con una peticion de actualización. Espera a que se apruebe o rechace'
                )
                return cleaned_data

        else:
            peticion = UpdateRequest(user=user)
            peticion.save()

        changed_data = self.changed_data
        for field in changed_data:
            data[field] = cleaned_data[field]

        cleaned_data['changed_fields'] = self.changed_data
        cleaned_data['changed'] = data
        return cleaned_data

class AuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(
            attrs={'placeholder': 'Correo electrónico'})
        self.fields['username'].label = False
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'placeholder': 'Contraseña'})
        self.fields['password'].label = False


"""
CBV para los formularios estaticos
"""
class ArticuloForm(ModelForm):
    error_css_class = 'error'
    publicacion = forms.DateField(label="Fecha de publicación", help_text='Solo si se encuentra Publicado', input_formats=[
                                  '%d-%m-%Y'], required=False)

    class Meta:
        model = Articulo
        fields = '__all__'
        labels = {
            'categoria': 'Categoría',
            'primer_autor': 'Autor',
            'palabras_clave': 'Palabras clave',
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'pais': 'País',
            'isnn': 'ISNN',
            'url': 'Dirección URL',
            'estado': 'Estado actual',
            'pagina_inicio': 'De la página',
            'pagina_fin': 'a la página',
            'lineas_investigacion': 'Lineas de investigación',
            'doi': 'DOI',
            'indice_revista': 'Índice de registro de revista'
        }
        help_texts = {
            'indice_revista': 'Solo si es indizada',
            # 'pagina_inicio': 'Solo si es Capítulo',
            # 'pagina_fin': 'Solo si es Capítulo',
            'palabras_clave': 'Mínimo tres',
            'lineas_investigacion': 'Mínimo una',
            'isnn': '(Número Internacional Normalizado de Publicaciones Seriadas)',
            'doi': 'Identificador de objeto digital'
        }

    def clean(self):
        cleaned_data = super(ArticuloForm, self).clean()
        
        primer_autor = cleaned_data.get('primer_autor')
        primer_coautor = cleaned_data.get('primer_coautor')
        segundo_coautor = cleaned_data.get('segundo_coautor')
        if segundo_coautor:
            if not primer_coautor:
                self.add_error(
                    'segundo_coautor', 'No puedes tener un segundo coautor sin un primer coautor')

        if primer_coautor:
            if primer_autor == primer_coautor:
                self.add_error(
                'primer_coautor', 'El autor y los coautores no pueden ser la misma persona')

            if segundo_coautor:
                if primer_coautor == segundo_coautor:
                    self.add_error(
                        'segundo_coautor', 'El autor y los coautores no pueden ser la misma persona')

        if segundo_coautor:
            if primer_autor == segundo_coautor:
                self.add_error(
                    'segundo_coautor', 'El autor y los coautores no pueden ser la misma persona')
            if primer_coautor:
                if segundo_coautor == primer_coautor:
                    self.add_error(
                        'segundo_coautor', 'El autor y los coautores no pueden ser la misma persona')


        pagina_inicio = cleaned_data.get('pagina_inicio')
        pagina_fin = cleaned_data.get('pagina_fin')
        if pagina_inicio:
            if not pagina_fin:
                self.add_error(
                'pagina_fin', 'Debes seleccionar una pagina de fin')

        if pagina_fin:
            if not pagina_inicio:
                self.add_error(
                'pagina_fin', 'Debes seleccionar una pagina de fin')
        
        if pagina_inicio and pagina_fin:
            if pagina_fin < pagina_inicio:
                self.add_error(
                    'pagina_inicio', 'La pagina de inicio no puede ser mayor a la pagina de fin')

        estado = cleaned_data.get('estado')
        publicacion = cleaned_data.get('publicacion')
        pais = cleaned_data.get('pais')
        revista = cleaned_data.get('revista')
        editorial = cleaned_data.get('editorial')
        isnn = cleaned_data.get('isnn')
        if estado == 'A':
            if pais:
                self.add_error(
                    'pais', 'No puedes agregar un pais si no se encuentra publicado')
            if editorial:
                self.add_error(
                    'editorial', 'No puedes agregar una editorial si no se encuentra publicado')
            if revista:
                self.add_error(
                    'revista', 'No puedes agregar una revista si no se encuentra publicado')
            if isnn:
                self.add_error(
                    'isnn', 'No puedes agregar el ISNN si no se encuentra publicado')
            if publicacion:
                self.add_error(
                    'publicacion', 'No puedes agregar una fecha de publicación a un articulo no publicado')
        else:

            if not pais:
                self.add_error(
                    'pais', 'Debes agregar un pais')
            if not editorial:
                self.add_error(
                    'editorial', 'Debes agregar una editorial')
            if not revista:
                self.add_error(
                    'revista', 'Debes agregar una revista')
            if not isnn:
                self.add_error(
                    'isnn', 'Debes agregar el ISNN')
            if not publicacion:
                self.add_error(
                    'publicacion', 'Debes agregar una fecha de publicación')
                    
        palabras_clave = cleaned_data.get('palabras_clave')
        if palabras_clave.count() < 3:
            self.add_error('palabras_clave',
                           'Debes escoger al menos 3 palabras clave')

        lineas_investigacion = cleaned_data.get('lineas_investigacion')
        if lineas_investigacion.count() == 0:
            self.add_error('lineas_investigacion',
                           'Debes escoger al menos 1 linea de investigacion')

        categoria = cleaned_data.get('categoria')
        indice_revista = cleaned_data.get('indice_revista')
        if categoria == 'IND' or categoria == 'JCR':
            if not indice_revista:
                self.add_error(
                    'indice_revista', 'Los articulos INDIZADOS o JCR deben tener un indice de revista')

        return cleaned_data

class CapituloLibroForm(ModelForm):
    publicacion = forms.DateField(label="Fecha de publicación", help_text='Solo si se encuentra Publicado', input_formats=[
                                  '%d-%m-%Y'], required=False)

    class Meta:
        model = CapituloLibro
        fields = '__all__'
        labels = {
            'categoria': 'Categoría',
            'primer_autor': 'Autor',
            'palabras_clave': 'Palabras clave',
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'pais': 'País',
            'isnn': 'ISNN',
            'url': 'Dirección URL',
            'estado': 'Estado actual',
            'pagina_inicio': 'De la página',
            'pagina_fin': 'a la página',
            'lineas_investigacion': 'Lineas de investigación',
            'doi': 'DOI',
            'indice_revista': 'Índice de registro de revista',
            'edicion': 'Edición',
            'isbn': 'ISBN',
            'proposito': 'Propósito'
        }

        help_texts = {
            'indice_revista': 'Solo si es indizada',
            'pagina_inicio': 'Solo si es Capítulo',
            'pagina_fin': 'Solo si es Capítulo',
            'palabras_clave': 'Mínimo tres',
            'lineas_investigacion': 'Mínimo una',
            'isbn': '(Número Estándar Internacional de Libros)',
            'titulo': 'Del libro o capítulo',
            'doi': 'Identificador de objeto digital'
        }

    def clean(self):

        cleaned_data = super(CapituloLibroForm, self).clean()

        

        primer_autor = cleaned_data.get('primer_autor')
        primer_coautor = cleaned_data.get('primer_coautor')
        segundo_coautor = cleaned_data.get('segundo_coautor')
        if segundo_coautor:
            if not primer_coautor:
                self.add_error(
                    'segundo_coautor', 'No puedes tener un segundo coautor sin un primer coautor')

        if primer_coautor:
            if primer_autor == primer_coautor:
                self.add_error(
                'primer_coautor', 'El autor y los coautores no pueden ser la misma persona')

            if segundo_coautor:
                if primer_coautor == segundo_coautor:
                    self.add_error(
                        'segundo_coautor', 'El autor y los coautores no pueden ser la misma persona')

        if segundo_coautor:
            if primer_autor == segundo_coautor:
                self.add_error(
                    'segundo_coautor', 'El autor y los coautores no pueden ser la misma persona')
            if primer_coautor:
                if segundo_coautor == primer_coautor:
                    self.add_error(
                        'segundo_coautor', 'El autor y los coautores no pueden ser la misma persona')

        tipo = cleaned_data.get('tipo')
        pagina_inicio = cleaned_data.get('pagina_inicio')
        pagina_fin = cleaned_data.get('pagina_fin')
        if tipo == 'L':
            if pagina_inicio or pagina_fin:
                self.add_error(
                    'pagina_inicio', 'Un libro no debería tener pagina de inicio ni de fin')
        else:
            if not pagina_inicio or not pagina_fin:
                self.add_error(
                    'pagina_inicio', 'El capitulo necesita una pagina de inicio y de fin')
            if pagina_inicio and pagina_fin:
                if pagina_fin < pagina_inicio:
                    self.add_error(
                        'pagina_inicio', 'La pagina de inicio no puede ser mayor a la pagina de fin')

        estado = cleaned_data.get('estado')
        publicacion = cleaned_data.get('publicacion')
        pais = cleaned_data.get('pais')
        editorial = cleaned_data.get('editorial')
        edicion = cleaned_data.get('edicion')
        tiraje = cleaned_data.get('tiraje')
        isbn = cleaned_data.get('isbn')
        

        if estado == 'A':
            if pais:
                self.add_error(
                    'pais', 'No puedes agregar un pais si no se encuentra publicado')
            if editorial:
                self.add_error(
                    'editoria', 'No puedes agregar una editorial si no se encuentra publicado')
            if edicion:
                self.add_error(
                    'edicion', 'No puedes agregar una edicion si no se encuentra publicado')
            if tiraje:
                self.add_error(
                    'tiraje', 'No puedes agregar un numero de tiraje si no se encuentra publicado')
            if isbn:
                self.add_error(
                    'isbn', 'No puedes agregar el ISBN si no se encuentra publicado')

            if publicacion:
                self.add_error(
                    'publicacion', 'No puedes agregar una fecha de publicación a un articulo no publicado')
        else:

            if not pais:
                self.add_error(
                    'pais', 'Debes agregar un pais')
            if not editorial:
                self.add_error(
                    'editorial', 'Debes agregar una editorial')
            if not edicion:
                self.add_error(
                    'edicion', 'Debes agregar un numero de edicion')
            if not tiraje:
                self.add_error(
                    'tiraje', 'Debes agregar un numero de tiraje')
            if not isbn:
                self.add_error(
                    'isbn', 'Debes agregar el ISBN')
            if not publicacion:
                self.add_error(
                    'publicacion', 'Debes agregar una fecha de publicación')

        if isbn:
            if len(isbn) > 15 and len(isbn) < 12:
                self.add_error(
                    'isbn', 'El ISBN debe tener entre 12 y 15 caracteres')

        palabras_clave = cleaned_data.get('palabras_clave')
        if palabras_clave.count() < 3:
            self.add_error('palabras_clave',
                           'Debes escoger al menos 3 palabras clave')

        lineas_investigacion = cleaned_data.get('lineas_investigacion')
        if lineas_investigacion.count() == 0:
            self.add_error('lineas_investigacion',
                           'Debes escoger al menos 1 línea de investigación')

        categoria = cleaned_data.get('categoria')
        indice_revista = cleaned_data.get('indice_revista')
        if categoria == 'IND' or categoria == 'JCR':
            if not indice_revista:
                self.add_error(
                    'indice_revista', 'Los articulos INDIZADOS o JCR deben tener un indice de revista')

        return cleaned_data

class PatenteForm(ModelForm):
    publicacion = forms.DateField(label="Fecha de publicación", input_formats=[
                                  '%d-%m-%Y'], required=False)

    class Meta:
        model = Patente
        fields = '__all__'
        labels = {
            'categoria': 'Categoría',
            'primer_autor': 'Autor',
            'palabras_clave': 'Palabras clave',
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'pais': 'País',
            'isnn': 'ISNN',
            'url': 'Dirección URL',
            'estado': 'Estado actual',
            'pagina_inicio': 'De la página',
            'pagina_fin': 'a la página',
            'lineas_investigacion': 'Lineas de investigación',
            'doi': 'DOI',
            'indice_revista': 'Índice de registro de revista',
            'edicion': 'Edición',
            'isbn': 'ISBN',
            'proposito': 'Propósito',
            'registro': 'Número de patente'
        }

        help_texts = {
            'autores': 'Selecciona uno o varios',
            'indice_revista': 'Solo si es indizada',
            'pagina_inicio': 'Solo si es Capítulo',
            'pagina_fin': 'Solo si es Capítulo',
            'palabras_clave': 'Mínimo tres',
            'lineas_investigacion': 'Mínimo una',
            'isbn': '(Número Estándar Internacional de Libros)',
            'doi': 'Identificador de objeto digital',
            'registro': 'Numero de registro según el país',
            'pais': 'País donde se registro la patente'
        }

class CongresoForm(ModelForm):
    publicacion = forms.DateField(label='Fecha de publicación', input_formats=[
                                  '%d-%m-%Y'], required=False)
    presentacion = forms.DateField(label='Fecha de presentación', input_formats=[
                                   '%d-%m-%Y'], required=True)

    class Meta:
        model = Congreso
        fields = '__all__'
        labels = {
            'primer_autor': 'Autor',
            'estadoP': 'Estado',
            'categoria': 'Categoría',
            'primer_autor': 'Autor',
            'palabras_clave': 'Palabras clave',
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'pais': 'País',
            'isnn': 'ISNN',
            'url': 'Dirección URL',
            'estado': 'Estado actual',
            'pagina_inicio': 'De la página',
            'pagina_fin': 'a la página',
            'lineas_investigacion': 'Lineas de investigación',
            'doi': 'DOI',
            'indice_revista': 'Índice de registro de revista',
            'edicion': 'Edición',
            'isbn': 'ISBN',
            'proposito': 'Propósito',
            'registro': 'Número de patente',
        }

        help_texts = {
            'autores': 'Selecciona uno o varios',
            'indice_revista': 'Solo si es indizada',
            'pagina_inicio': 'Solo si es Capítulo',
            'pagina_fin': 'Solo si es Capítulo',
            'palabras_clave': 'Mínimo tres',
            'lineas_investigacion': 'Mínimo una',
            'isbn': '(Número Estándar Internacional de Libros)',
            'doi': 'Identificador de objeto digital',
            'registro': 'Numero de registro según el país',
            'pais': 'País donde se registro la patente',
            'estadoP': 'Estados del pais. Solo disponibles para México',
            'ciudad': 'Ciudades de estados. Solo disponibles para México',
        }

    def clean(self):

        cleaned_data = super(CongresoForm, self).clean()
        primer_autor = cleaned_data.get('primer_autor')
        primer_colaborador = cleaned_data.get('primer_colaborador')
        segundo_colaborador = cleaned_data.get('segundo_colaborador')
        if segundo_colaborador:
            if not primer_colaborador:
                self.add_error(
                    'segundo_colaborador', 'No puedes tener un segundo colaborador sin un primer colaborador')

        # if primer_autor == primer_colaborador or primer_autor == segundo_colaborador or primer_colaborador == segundo_colaborador:
        #     self.add_error(
        #         'primer_autor', 'El autor y los colaboradores no pueden ser la misma persona')

        estado = cleaned_data.get('estado')
        publicacion = cleaned_data.get('publicacion')
        if estado == 'A':
            if publicacion:
                self.add_error(
                    'publicacion', 'No puedes agregar una fecha de publicacion a un articulo no publicado')
        else:
            if not publicacion:
                self.add_error(
                    'publicacion', 'Debes agregar una fecha de publicacion')

        palabras_clave = cleaned_data.get('palabras_clave')
        if palabras_clave.count() < 3:
            self.add_error('palabras_clave',
                           'Debes escoger al menos 3 palabras clave')

        lineas_investigacion = cleaned_data.get('lineas_investigacion')
        if lineas_investigacion.count() == 0:
            self.add_error('lineas_investigacion',
                           'Debes escoger al menos 1 linea de investigacion')

        presentacion = cleaned_data.get('presentacion')
        if presentacion and publicacion:
            if presentacion > publicacion:
                self.add_error(
                    'presentacion', 'La fecha de presentacion no puede ser mayor a la fecha de publicacion')

        pais = cleaned_data.get('pais')
        if str(pais) == 'México':
            estadoP = cleaned_data.get('estadoP')
            if not estadoP:
                self.add_error('estadoP', 'Necesitas seleccionar un estado')

        return cleaned_data

class InvestigacionForm(ModelForm):
    inicio = forms.DateField(label='Fecha de inicio', input_formats=[
                             '%d-%m-%Y'], required=True)
    fin = forms.DateField(label='Fecha de fin', input_formats=[
                          '%d-%m-%Y'], required=True)

    class Meta:
        model = Investigacion
        fields = '__all__'
        labels = {
            'tipo_proyecto': 'Tipo de proyecto',
            'financiamiento': '¿Tuvó financiamiento?',
            'tipo_financiamiento': 'Tipo de financiamiento',
            'primer_autor': 'Autor',
            'estadoP': 'Estado',
            'categoria': 'Categoría',
            'primer_autor': 'Autor',
            'palabras_clave': 'Palabras clave',
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'pais': 'País',
            'isnn': 'ISNN',
            'url': 'Dirección URL',
            'estado': 'Estado actual',
            'pagina_inicio': 'De la página',
            'pagina_fin': 'a la página',
            'lineas_investigacion': 'Lineas de investigación',
            'doi': 'DOI',
            'indice_revista': 'Índice de registro de revista',
            'edicion': 'Edición',
            'isbn': 'ISBN',
            'proposito': 'Propósito',
            'registro': 'Número de patente',
        }

        help_texts = {
            'autores': 'Selecciona uno o varios',
            'indice_revista': 'Solo si es indizada',
            'pagina_inicio': 'Solo si es Capítulo',
            'pagina_fin': 'Solo si es Capítulo',
            'palabras_clave': 'Mínimo tres',
            'lineas_investigacion': 'Mínimo una',
            'isbn': '(Número Estándar Internacional de Libros)',
            'doi': 'Identificador de objeto digital',
            'registro': 'Numero de registro según el país',
            'pais': 'País donde se registro la patente',
            'estadoP': 'Estados del pais. Solo disponibles para México',
            'ciudad': 'Ciudades de estados. Solo disponibles para México',
            'resumen': 'Archivo de máximo 25MB en formato PDF'
        }

    def clean(self):
        cleaned_data = super(InvestigacionForm, self).clean()
        financiamiento = cleaned_data.get('financiamiento')
        tipo_financiamiento = cleaned_data.get('tipo_financiamiento')
        if financiamiento:
            if not tipo_financiamiento:
                self.add_error('tipo_financiamiento',
                               'Debes escoger un tipo de financiamiento')
        else:
            if tipo_financiamiento:
                self.add_error(
                    'tipo_financiamiento', 'No puedes escoger un tipo de financimiento si no tienes financiamiento')

        responsable = cleaned_data.get('responsable')
        primer_colaborador = cleaned_data.get('primer_colaborador')
        segundo_colaborador = cleaned_data.get('segundo_colaborador')

        if segundo_colaborador:
            if not primer_colaborador:
                self.add_error(
                    'primer_colaborador', 'No puedes tener un segundo colaborador sin un primer colaborador')

        if primer_colaborador:
            if responsable == primer_colaborador:
                self.add_error(
                    'responsable', 'El responsable y los colaboradores no pueden ser la misma persona')
            if segundo_colaborador:
                if primer_colaborador == segundo_colaborador:
                    self.add_error(
                        'responsable', 'El responsable y los colaboradores no pueden ser la misma persona')

                if responsable == segundo_colaborador:
                    self.add_error(
                        'responsable', 'El responsable y los colaboradores no pueden ser la misma persona')

        if segundo_colaborador:
            if not primer_colaborador:
                self.add_error(
                    'primer_colaborador', 'No puedes tener un segundo alumno sin un primer alumno')

        primer_alumno = cleaned_data.get('primer_alumno')
        segundo_alumno = cleaned_data.get('segundo_alumno')
        tercer_alumno = cleaned_data.get('tercer_alumno')
        if segundo_alumno:
            if not primer_alumno:
                self.add_error(
                    'segundo_alumno', 'No puedes tener un segundo alumno sin un primer alumno')

        if tercer_alumno:
            if not segundo_alumno or not primer_alumno:
                self.add_error(
                    'tercer_alumno', 'No puedes tener un tercer alumno sin un primero ni segundo alumno')

        if primer_alumno and segundo_alumno:
            if primer_alumno == segundo_alumno:
                self.add_error('primer_alumno',
                               'Los alumnos no pueden ser la misma persona')

        if primer_alumno and tercer_alumno:
            if primer_alumno == tercer_alumno:
                self.add_error('primer_alumno',
                               'Los alumnos no pueden ser la misma persona')

        if segundo_alumno and tercer_alumno:
            if segundo_alumno == tercer_alumno:
                self.add_error('primer_alumno',
                               'Los alumnos no pueden ser la misma persona')

        palabras_clave = cleaned_data.get('palabras_clave')
        if palabras_clave.count() < 3:
            self.add_error('palabras_clave',
                           'Debes escoger al menos 3 palabras clave')

        lineas_investigacion = cleaned_data.get('lineas_investigacion')
        if lineas_investigacion.count() == 0:
            self.add_error('lineas_investigacion',
                           'Debes escoger al menos 1 linea de investigacion')

        inicio = cleaned_data.get('inicio')
        fin = cleaned_data.get('fin')
        if inicio and fin:
            if inicio > fin:
                self.add_error(
                    'inicio', 'La fecha de inicio no puede ser mayor a la fecha de fin')

        return cleaned_data

class TesisForm(ModelForm):
    inicio = forms.DateField(label='Fecha de inicio', input_formats=[
                             '%d-%m-%Y'], required=True)
    fin = forms.DateField(label='Fecha de fin', input_formats=[
                          '%d-%m-%Y'], required=True)

    class Meta:
        model = Tesis
        fields = '__all__'
        widgets = {
            'profesor': forms.HiddenInput()
        }
        labels = {
            'tipo_proyecto': 'Tipo de proyecto',
            'institucion': 'Institución',
            'profesor': None,
            'financiamiento': '¿Tuvó financiamiento?',
            'tipo_financiamiento': 'Tipo de financiamiento',
            'primer_autor': 'Autor',
            'estadoP': 'Estado',
            'categoria': 'Categoría',
            'primer_autor': 'Autor',
            'palabras_clave': 'Palabras clave',
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'pais': 'País',
            'isnn': 'ISNN',
            'url': 'Dirección URL',
            'estado': 'Estado actual',
            'pagina_inicio': 'De la página',
            'pagina_fin': 'a la página',
            'lineas_investigacion': 'Lineas de investigación',
            'doi': 'DOI',
            'indice_revista': 'Índice de registro de revista',
            'edicion': 'Edición',
            'isbn': 'ISBN',
            'proposito': 'Propósito',
            'registro': 'Número de patente',
        }

        help_texts = {
            'autores': 'Selecciona uno o varios',
            'indice_revista': 'Solo si es indizada',
            'pagina_inicio': 'Solo si es Capítulo',
            'pagina_fin': 'Solo si es Capítulo',
            'palabras_clave': 'Mínimo tres',
            'lineas_investigacion': 'Mínimo una',
            'isbn': '(Número Estándar Internacional de Libros)',
            'doi': 'Identificador de objeto digital',
            'registro': 'Numero de registro según el país',
            'pais': 'País donde se registro la patente',
            'estadoP': 'Estados del pais. Solo disponibles para México',
            'ciudad': 'Ciudades de estados. Solo disponibles para México',
            'resumen': 'Archivo de máximo 25MB en formato PDF'
        }

    def clean(self):
        cleaned_data = super(TesisForm, self).clean()

        inicio = cleaned_data.get('inicio')
        fin = cleaned_data.get('fin')
        if inicio and fin:
            if inicio > fin:
                self.add_error(
                    'inicio', 'La fecha de inicio no puede ser mayor a la fecha de fin')

        palabras_clave = cleaned_data.get('palabras_clave')
        if palabras_clave.count() < 3:
            self.add_error('palabras_clave',
                           'Debes escoger al menos 3 palabras clave')

        lineas_investigacion = cleaned_data.get('lineas_investigacion')
        if lineas_investigacion.count() == 0:
            self.add_error('lineas_investigacion',
                           'Debes escoger al menos 1 linea de investigacion')

        return cleaned_data


"""
CBV para los formularios Popup
"""
class AutorForm(ModelForm):
    id_field = forms.CharField(
        max_length=30, required=True, widget=forms.HiddenInput)

    class Meta:
        model = Autor
        fields = ['first_name', 'last_name']
        labels = {
            'first_name':'Nombre(s)',
            'last_name':'Apellido(s)'
        }

    def clean(self):
        cleaned_data = super(AutorForm, self).clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        # user = cleaned_data.get('user')
        autor_existente = Autor.objects.filter(
            Q(first_name=first_name, last_name=last_name) |
            Q(user__first_name=first_name, user__last_name=last_name)
        ).count()

        if first_name is None or last_name is None:
                raise forms.ValidationError('Debe crear un autor con nombre(s) y apellido(s)')

        if autor_existente > 0:
            self.add_error(
                'first_name', 'Un autor con los mismos datos ya existe. Elíjalo o verifique sus datos')

        if len(first_name) <= LONGITUD_NOMBRE_AUTOR:
            self.add_error(
                'first_name', 'El nombre debe ser mayor a 1 carácter')

        if len(last_name) <= LONGITUD_APELLIDO_AUTOR:
            self.add_error(
                'last_name', 'El apellido debe ser mayor a 1 carácter')

class RevistaForm(ModelForm):
    id_field = forms.CharField(
        max_length=30, required=True, widget=forms.HiddenInput)

    class Meta:
        model = Revista
        fields = '__all__'
        error_messages = {
            'nombre': {
                'unique': 'Una revista con este nombre ya existe. Elíjala o verifique sus datos'
            }
        }

class EditorialForm(ModelForm):
    id_field = forms.CharField(
        max_length=30, required=True, widget=forms.HiddenInput)

    class Meta:
        model = Editorial
        fields = '__all__'
        error_messages = {
            'nombre': {
                'unique': 'Una editorial con este nombre ya existe. Elíjala o verifique sus datos'
            }
        }

class PalabrasForm(ModelForm):
    id_field = forms.CharField(
        max_length=30, required=True, widget=forms.HiddenInput)

    class Meta:
        model = PalabrasClave
        fields = '__all__'
        error_messages = {
            'nombre': {
                'unique': 'Una palabra clave con este nombre ya existe. Elíjala o verifique sus datos'
            }
        }

class LineasForm(ModelForm):
    id_field = forms.CharField(
        max_length=30, required=True, widget=forms.HiddenInput)

    class Meta:
        model = LineaInvestigacion
        fields = '__all__'
        error_messages = {
            'nombre': {
                'unique': 'Una línea de investigación con este nombre ya existe. Elíjala o verifique sus datos'
            }
        }

class AlumnoForm(ModelForm):
    id_field = forms.CharField(
        max_length=30, required=True, widget=forms.HiddenInput)

    class Meta:
        model = Alumno
        fields = '__all__'

class InstitucionForm(ModelForm):
    id_field = forms.CharField(
        max_length=30, required=True, widget=forms.HiddenInput)

    class Meta:
        model = Institucion
        fields = '__all__'
        error_messages = {
            'nombre': {
                'unique': 'Una institución con este nombre ya existe. Elíjala o verifique sus datos'
            }
        }

class FacultadForm(ModelForm):
    id_field = forms.CharField(
        max_length=30, required=True, widget=forms.HiddenInput)

    class Meta:
        model = Facultad
        fields = '__all__'
        error_messages = {
            'nombre': {
                'unique': 'Una facultad con este nombre ya existe. Elíjala o verifique sus datos'
            }
        }

class NivelForm(ModelForm):
    id_field = forms.CharField(
        max_length=30, required=True, widget=forms.HiddenInput)

    class Meta:
        model = Nivel
        fields = '__all__'
        error_messages = {
            'nombre': {
                'unique': 'Un nivel con este nombre ya existe. Elíjalo o verifique sus datos'
            }
        }


class ContratoForm(ModelForm):
    id_field = forms.CharField(
        max_length=30, required=True, widget=forms.HiddenInput)

    class Meta:
        model = Contrato
        fields = '__all__'
        error_messages = {
            'nombre': {
                'unique': 'Un tipo de contrato con este nombre ya existe. Elíjalo o verifique sus datos'
            }
        }