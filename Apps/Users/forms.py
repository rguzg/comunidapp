from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.widgets import PasswordInput, TextInput
from .models import (Alumno, Articulo, Autor, CapituloLibro, Congreso,
                     Contrato, Editorial, Facultad, Institucion, Investigacion,
                     LineaInvestigacion, Nivel, PalabrasClave, Patente,
                     Revista, Tesis, User)


"""
CBV para los formularios de inicio de sesion y actualizacion de datos
"""
class UserActualizadoForm(forms.Form):
    error_css_class = "error"

    generos = [
        ('H', 'Hombre'),
        ('M', 'Mujer')
    ]

    grados = [
        ('L', 'Licenciatura'),
        ('M', 'Maestría'),
        ('D', 'Doctorado')
    ]

    email = forms.EmailField(required=True)
    clave = forms.IntegerField(required=True, max_value=5, min_value=1)
    sexo = forms.ChoiceField(required=True, choices=generos)
    nacimiento = forms.DateField(required=True, widget=forms.DateInput)
    foto = forms.ImageField(required=True)
    grado = forms.ChoiceField(required=True, choices=grados)
    contratacion = forms.ModelChoiceField(queryset=Contrato.objects.all())
    facultades = forms.ModelMultipleChoiceField(
        queryset=Facultad.objects.all(),
        widget=forms.CheckboxSelectMultiple,

    )
    niveles = forms.ModelMultipleChoiceField(
        queryset=Nivel.objects.all(),
        widget=forms.CheckboxSelectMultiple,

    )
    investigaciones = forms.ModelMultipleChoiceField(
        queryset=LineaInvestigacion.objects.all(),
        widget=forms.CheckboxSelectMultiple,

    )

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
    publicacion = forms.DateField(input_formats=['%d-%m-%Y'], required=False)

    class Meta:
        model = Articulo
        fields = '__all__'

    def clean(self):
        print('CLEANING ARTICULO FORM')
        cleaned_data = super(ArticuloForm, self).clean()
        # print(cleaned_data)
        primer_autor = cleaned_data.get('primer_autor')
        primer_colaborador = cleaned_data.get('primer_colaborador')
        segundo_colaborador = cleaned_data.get('segundo_colaborador')
        if segundo_colaborador:
            if not primer_colaborador:
                self.errors['segundo_colaborador'] = 'No puedes tener un segundo colaborador sin un primer colaborador'
                self.errors['segundo_colaborador'] = 'No puedes tener un segundo colaborador sin un primer colaborador'

        if primer_autor == primer_colaborador or primer_autor == segundo_colaborador or primer_colaborador == segundo_colaborador:
            #     'El autor y los colaboradores no pueden ser la misma persona')
            self.errors['primer_autor'] = 'El autor y los colaboradores no pueden ser la misma persona'
            

        pagina_inicio = cleaned_data.get('pagina_inicio')
        pagina_fin = cleaned_data.get('pagina_fin')
        if pagina_fin < pagina_inicio:
            # raise ValidationErro]r(
                # 'La pagina de inicio no puede ser mayor a la pagina de fin')
            self.errors['pagina_inicio'] = 'La pagina de inicio no puede ser mayor a la pagina de fin'

        estado = cleaned_data.get('estado')
        publicacion = cleaned_data.get('publicacion')
        if estado == 'A':
            if publicacion:
                # raise ValidationError(
                #     'No puedes agregar una fecha de publicacion a un articulo no publicado')
                self.errors['publicacion'] = 'No puedes agregar una fecha de publicacion a un articulo no publicado'
        else:
            if not publicacion:
                # raise ValidationError('Debes agregar una fecha de publicacion')
                self.errors['publicacion'] = 'Debes agregar una fecha de publicacion'

        palabras_clave = cleaned_data.get('palabras_clave')
        print(len(palabras_clave))
        print(palabras_clave.count())
        if palabras_clave.count() < 3:
            # raise ValidationError('Debes escoger al menos 3 palabras clave')
            self.errors['palabras_clave'] = 'Debes escoger al menos 3 palabras clave'

        lineas_investigacion = cleaned_data.get('lineas_investigacion')
        if lineas_investigacion.count() == 0:
            # raise ValidationError(
            #     'Debes escoger al menos 1 linea de investigacion')
            self.errors['lineas_investigacion'] = 'Debes escoger al menos 1 linea de investigacion'

        categoria = cleaned_data.get('categoria')
        indice_revista = cleaned_data.get('indice_revista')
        if categoria == 'IND' or categoria == 'JCR':
            if not indice_revista:
                # raise ValidationError(
                #     'Los articulos INDIZADOS o JCR deben tener un indice de revista')
                self.errors['indice_revista'] = 'Los articulos INDIZADOS o JCR deben tener un indice de revista'

        return cleaned_data

class CapituloLibroForm(ModelForm):
    publicacion = forms.DateField(input_formats=['%d-%m-%Y'], required=False)

    class Meta:
        model = CapituloLibro
        fields = '__all__'

    def clean(self):

        cleaned_data = super(CapituloLibroForm, self).clean()

        isbn = cleaned_data.get('isbn')
        if len(isbn) > 15 and len(isbn) < 12:
            # raise ValidationError('El ISBN debe tener entre 12 y 15 caracteres')
            self.errors['ISBN'] = 'El ISBN debe tener entre 12 y 15 caracteres'
        
        primer_autor = cleaned_data.get('primer_autor')
        primer_coautor = cleaned_data.get('primer_coautor')
        segundo_coautor = cleaned_data.get('segundo_coautor')
        if segundo_coautor:
            if not primer_coautor:
                # raise ValidationError(
                #     'No puedes tener un segundo coautor sin un primer coautor')
                self.errors['segundo_coautor'] = 'No puedes tener un segundo coautor sin un primer coautor'

        if primer_autor == primer_coautor or primer_autor == segundo_coautor or primer_coautor == segundo_coautor:
            # raise ValidationError(
            #     'El autor y los coautores no pueden ser la misma persona')
            self.errors['primer_autor'] = 'El autor y los coautores no pueden ser la misma persona'

        tipo = cleaned_data.get('tipo')
        pagina_inicio = cleaned_data.get('pagina_inicio')
        pagina_fin = cleaned_data.get('pagina_fin')
        if tipo == 'L':
            if pagina_inicio or pagina_fin:
                # raise ValidationError(
                #     'Un libro no deberia tener pagina de inicio ni de fin')
                self.errors['pagina_inicio'] = 'Un libro no debería tener pagina de inicio ni de fin'
        else:
            if not pagina_inicio or not pagina_fin:
                # raise ValidationError(
                    # 'El capitulo necesita una pagina de inicio y de fin')
                self.errors['pagina_inicio'] = 'El capitulo necesita una pagina de inicio y de fin'
            if pagina_fin < pagina_inicio:
                # raise ValidationError(
                #     'La pagina de inicio no puede ser mayor a la pagina de fin')
                self.errors['pagina_inicio'] = 'La pagina de inicio no puede ser mayor a la pagina de fin'

        estado = cleaned_data.get('estado')
        publicacion = cleaned_data.get('publicacion')
        if estado == 'A':
            if publicacion:
                # raise ValidationError(
                    # 'No puedes agregar una fecha de publicacion a un articulo no publicado')
                self.errors['publicacion'] = 'No puedes agregar una fecha de publicación a un articulo no publicado'
        else:
            if not publicacion:
                # raise ValidationError('Debes agregar una fecha de publicacion')
                self.errors['publicacion'] = 'Debes agregar una fecha de publicación'

        palabras_clave = cleaned_data.get('palabras_clave')
        # print(len(palabras_clave))
        # print(palabras_clave.count())
        if palabras_clave.count() < 3:
            # raise ValidationError('Debes escoger al menos 3 palabras clave')
            self.errors['palabras_clave'] = 'Debes escoger al menos 3 palabras clave'

        lineas_investigacion = cleaned_data.get('lineas_investigacion')
        if lineas_investigacion.count() == 0:
            # raise ValidationError(
                # 'Debes escoger al menos 1 linea de investigacion')
            self.errors['lineas_investigacion'] = 'Debes escoger al menos 1 línea de investigación'

        categoria = cleaned_data.get('categoria')
        indice_revista = cleaned_data.get('indice_revista')
        if categoria == 'IND' or categoria == 'JCR':
            if not indice_revista:
                # raise ValidationError(
                    # 'Los articulos INDIZADOS o JCR deben tener un indice de revista')
                self.errors['indice_revista'] = 'Los articulos INDIZADOS o JCR deben tener un indice de revista'

        return cleaned_data

class PatenteForm(ModelForm):
    publicacion = forms.DateField(input_formats=['%d-%m-%Y'], required=True)

    class Meta:
        model = Patente
        fields = '__all__'

class CongresoForm(ModelForm):
    publicacion = forms.DateField(input_formats=['%d-%m-%Y'], required=False)
    presentacion = forms.DateField(input_formats=['%d-%m-%Y'], required=True)

    class Meta:
        model = Congreso
        fields = '__all__'

    def clean(self):

        cleaned_data = super(CongresoForm, self).clean()
        # print(cleaned_data)
        primer_autor = cleaned_data.get('primer_autor')
        primer_colaborador = cleaned_data.get('primer_colaborador')
        segundo_colaborador = cleaned_data.get('segundo_colaborador')
        if segundo_colaborador:
            if not primer_colaborador:
                # raise ValidationError(
                #     'No puedes tener un segundo colaborador sin un primer colaborador')
                self.errors['segundo_colaborador'] = 'No puedes tener un segundo colaborador sin un primer colaborador'

        if primer_autor == primer_colaborador or primer_autor == segundo_colaborador or primer_colaborador == segundo_colaborador:
            # raise ValidationError(
            #     'El autor y los colaboradores no pueden ser la misma persona')
            self.errors['primer_autor'] = 'El autor y los colaboradores no pueden ser la misma persona'

        estado = cleaned_data.get('estado')
        publicacion = cleaned_data.get('publicacion')
        if estado == 'A':
            if publicacion:
                # raise ValidationError(
                #     'No puedes agregar una fecha de publicacion a un articulo no publicado')
                self.errors['publicacion'] = 'No puedes agregar una fecha de publicacion a un articulo no publicado'
        else:
            if not publicacion:
                # raise ValidationError('Debes agregar una fecha de publicacion')
                self.errors['publicacion'] = 'Debes agregar una fecha de publicacion'

        palabras_clave = cleaned_data.get('palabras_clave')
        if palabras_clave.count() < 3:
            # raise ValidationError('Debes escoger al menos 3 palabras clave')
            self.errors['palabras_clave'] = 'Debes escoger al menos 3 palabras clave'

        lineas_investigacion = cleaned_data.get('lineas_investigacion')
        if lineas_investigacion.count() == 0:
            # raise ValidationError(
                # 'Debes escoger al menos 1 linea de investigacion')
            self.errors['lineas_investigacion'] = 'Debes escoger al menos 1 linea de investigacion'

        presentacion = cleaned_data.get('presentacion')
        if presentacion and publicacion:
            if presentacion > publicacion:
                # raise ValidationError(
                    # 'La fecha de presentacion no puede ser mayor a la fecha de publicacion')
                self.errors['presentacion'] = 'La fecha de presentacion no puede ser mayor a la fecha de publicacion'

        pais = cleaned_data.get('pais')
        print(pais)
        if str(pais) == 'México':
            print("entro")
            estadoP = cleaned_data.get('estadoP')
            print(estadoP)
            if not estadoP:
                self.errors['estadoP'] = 'Necesitas seleccionar un estado'
                

        
        

        return cleaned_data

class InvestigacionForm(ModelForm):
    inicio = forms.DateField(input_formats=['%d-%m-%Y'], required=True)
    fin = forms.DateField(input_formats=['%d-%m-%Y'], required=True)

    class Meta:
        model = Investigacion
        fields = '__all__'

    def clean(self):
        cleaned_data = super(InvestigacionForm, self).clean()
        financiamiento = cleaned_data.get('financiamiento')
        tipo_financiamiento = cleaned_data.get('tipo_financiamiento')
        if financiamiento:
            if not tipo_financiamiento:
                # raise ValidationError(
                #     'Debes escoger un tipo de financiamiento')
                self.errors['tipo_financiamiento'] = 'Debes escoger un tipo de financiamiento'
        else:
            if tipo_financiamiento:
                # raise ValidationError(
                    # 'No puedes escoger un tipo de financimiento si no tienes financiamiento')
                self.errors['tipo_financiamiento'] = 'No puedes escoger un tipo de financimiento si no tienes financiamiento'

        responsable = cleaned_data.get('responsable')
        primer_colaborador = cleaned_data.get('primer_colaborador')
        segundo_colaborador = cleaned_data.get('segundo_colaborador')

        if segundo_colaborador:
            if not primer_colaborador:
                # raise ValidationError(
                    # 'No puedes tener un segundo colaborador sin un primer colaborador')
                self.errors['primer_colaborador'] = 'No puedes tener un segundo colaborador sin un primer colaborador'

        if primer_colaborador:
            if responsable == primer_colaborador:
                self.errors['responsable'] = 'El responsable y los colaboradores no pueden ser la misma persona'
            if segundo_colaborador:
                if primer_colaborador == segundo_colaborador:
                    self.errors['responsable'] = 'El responsable y los colaboradores no pueden ser la misma persona'
                
                if responsable == segundo_colaborador:
                    self.errors['responsable'] = 'El responsable y los colaboradores no pueden ser la misma persona'

        if segundo_colaborador:
            if not primer_colaborador:
                self.errors['primer_colaborador'] = 'No puedes tener un segundo alumno sin un primer alumno'
            
        
        primer_alumno = cleaned_data.get('primer_alumno')
        segundo_alumno = cleaned_data.get('segundo_alumno')
        tercer_alumno = cleaned_data.get('tercer_alumno')
        if segundo_alumno:
            if not primer_alumno:
                self.errors['segundo_alumno'] = 'No puedes tener un segundo alumno sin un primer alumno'
        
        if tercer_alumno:
            if not segundo_alumno or not primer_alumno:
                self.errors['tercer_alumno'] = 'No puedes tener un tercer alumno sin un primero ni segundo alumno'

        if primer_alumno and segundo_alumno:
            if primer_alumno == segundo_alumno:
                self.errors['primer_alumno'] = 'Los alumnos no pueden ser la misma persona'
        
        if primer_alumno and tercer_alumno:
            if primer_alumno == tercer_alumno:
                self.errors['primer_alumno'] = 'Los alumnos no pueden ser la misma persona'

        if segundo_alumno and tercer_alumno:
            if segundo_alumno == tercer_alumno:
                self.errors['primer_alumno'] = 'Los alumnos no pueden ser la misma persona'
        
                

        palabras_clave = cleaned_data.get('palabras_clave')
        if palabras_clave.count() < 3:
            # raise ValidationError('Debes escoger al menos 3 palabras clave')
            self.errors['palabras_clave'] = 'Debes escoger al menos 3 palabras clave'

        lineas_investigacion = cleaned_data.get('lineas_investigacion')
        if lineas_investigacion.count() == 0:
            # raise ValidationError(
                # 'Debes escoger al menos 1 linea de investigacion')
            self.errors['lineas_investigacion'] = 'Debes escoger al menos 1 linea de investigacion'

        inicio = cleaned_data.get('inicio')
        fin = cleaned_data.get('fin')
        if inicio and fin:
            if inicio > fin:
                # raise ValidationError(
                    # 'La fecha de inicio no puede ser mayor a la fecha de fin')
                self.errors['inicio'] = 'La fecha de inicio no puede ser mayor a la fecha de fin'
                

        return cleaned_data

class TesisForm(ModelForm):
    inicio = forms.DateField(input_formats=['%d-%m-%Y'], required=True)
    fin = forms.DateField(input_formats=['%d-%m-%Y'], required=True)

    class Meta:
        model = Tesis
        fields = '__all__'
        widgets = {
            'profesor': forms.HiddenInput()
        }
    

    def clean(self):
        cleaned_data = super(TesisForm, self).clean()

        inicio = cleaned_data.get('inicio')
        fin = cleaned_data.get('fin')
        if inicio and fin:
            if inicio > fin:
                # raise ValidationError(
                    # 'La fecha de inicio no puede ser mayor a la fecha de fin')
                self.errors['inicio'] = 'La fecha de inicio no puede ser mayor a la fecha de fin'

        palabras_clave = cleaned_data.get('palabras_clave')
        if palabras_clave.count() < 3:
            # raise ValidationError('Debes escoger al menos 3 palabras clave')
            self.errors['palabras_clave'] = 'Debes escoger al menos 3 palabras clave'

        lineas_investigacion = cleaned_data.get('lineas_investigacion')
        if lineas_investigacion.count() == 0:
            # raise ValidationError(
                # 'Debes escoger al menos 1 linea de investigacion')
            self.errors['lineas_investigacion'] = 'Debes escoger al menos 1 linea de investigacion'

        return cleaned_data



"""
CBV para los formularios Popup
"""

class AutorForm(ModelForm):
    id_field = forms.CharField(max_length=30, required=True, widget=forms.HiddenInput)
    class Meta:
        model = Autor
        fields = ['first_name', 'last_name']

    def clean(self):
        cleaned_data = super(AutorForm, self).clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        user = cleaned_data.get('user')
        autor_existente = Autor.objects.filter(
            first_name=first_name, last_name=last_name).count()
        print(autor_existente)
        if autor_existente > 0:
            raise ValidationError(
                'Un autor con los mismos datos ya existe. Eligelo o verifica tus datos')

        if user is None:
            if first_name is None or last_name is None:
                raise ValidationError('Debes seleccionar un usuario o crear un autor externo con nombre(s) y apellido(s)')

        if len(first_name)<=3:
            raise ValidationError('El nombre debe ser mayor a 3 caracteres')

        if len(last_name)<=3:
            raise ValidationError('El apellido debe ser mayor a 3 caracteres')


class RevistaForm(ModelForm):
    id_field = forms.CharField(max_length=30, required=True, widget=forms.HiddenInput)
    # id_field = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = Revista
        fields = '__all__'

class EditorialForm(ModelForm):
    id_field = forms.CharField(max_length=30, required=True, widget=forms.HiddenInput)
    # id_field = forms.CharField(max_length=30, required=True)
    class Meta:
        model = Editorial
        fields = '__all__'

class PalabrasForm(ModelForm):
    id_field = forms.CharField(max_length=30, required=True, widget=forms.HiddenInput)
    # id_field = forms.CharField(max_length=30, required=True)
    class Meta:
        model = PalabrasClave
        fields = '__all__'

class LineasForm(ModelForm):
    id_field = forms.CharField(max_length=30, required=True, widget=forms.HiddenInput)
    # id_field = forms.CharField(max_length=30, required=True)
    class Meta:
        model = LineaInvestigacion
        fields = '__all__'

class AlumnoForm(ModelForm):
    id_field = forms.CharField(max_length=30, required=True, widget=forms.HiddenInput)
    # id_field = forms.CharField(max_length=30, required=True)
    class Meta:
        model = Alumno
        fields = '__all__'

class InstitucionForm(ModelForm):
    id_field = forms.CharField(max_length=30, required=True, widget=forms.HiddenInput)
    # id_field = forms.CharField(max_length=30, required=True)
    class Meta:
        model = Institucion
        fields = '__all__'
