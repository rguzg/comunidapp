from django import forms
from django.forms import ModelForm
from .models import Contrato, Facultad, Nivel, LineaInvestigacion, User, Articulo,  CapituloLibro, Patente, Congreso, Investigacion, Tesis, Autor, Revista, Editorial, PalabrasClave
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.core.exceptions import ValidationError

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




class AutorForm(ModelForm):
    class Meta:
        model = Autor
        fields = ['first_name', 'last_name']

    def clean(self):
        cleaned_data=super(AutorForm, self).clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        autor_existente = Autor.objects.filter(first_name=first_name, last_name=last_name).count()
        if autor_existente == 0:
            raise ValidationError('Un autor con los mismos datos ya existe. Eligelo o verifica tus datos')

class RevistaForm(ModelForm):
    class Meta:
        model = Revista
        fields = '__all__'

class EditorialForm(ModelForm):
    class Meta:
        model = Editorial
        fields = '__all__' 

class PalabrasForm(ModelForm):
    class Meta:
        model = PalabrasClave
        fields = '__all__'



class ArticuloForm(ModelForm):
    publicacion = forms.DateField(input_formats=['%d-%m-%Y'], required=False)
    class Meta:
        model = Articulo
        fields = '__all__'

    def clean(self):
        cleaned_data = super(ArticuloForm, self).clean()
        # print(cleaned_data)
        primer_autor = cleaned_data.get('primer_autor')
        primer_colaborador = cleaned_data.get('primer_colaborador')
        segundo_colaborador = cleaned_data.get('segundo_colaborador')
        if segundo_colaborador:
            if not primer_colaborador:
                raise ValidationError('No puedes tener un segundo colaborador sin un primer colaborador')
                
        if primer_autor == primer_colaborador or primer_autor == segundo_colaborador or primer_colaborador == segundo_colaborador:
            raise ValidationError('El autor y los colaboradores no pueden ser la misma persona')

        pagina_inicio = cleaned_data.get('pagina_inicio')
        pagina_fin = cleaned_data.get('pagina_fin')
        if pagina_fin < pagina_inicio:
            raise ValidationError('La pagina de inicio no puede ser mayor a la pagina de fin')
        
        estado = cleaned_data.get('estado')
        publicacion = cleaned_data.get('publicacion')
        if estado == 'A':
            if publicacion:
                raise ValidationError('No puedes agregar una fecha de publicacion a un articulo no publicado')
        else:
            if not publicacion:
                raise ValidationError('Debes agregar una fecha de publicacion')
                
        palabras_clave = cleaned_data.get('palabras_clave')
        print(len(palabras_clave))
        print(palabras_clave.count())
        if palabras_clave.count() < 3:
            raise ValidationError('Debes escoger al menos 3 palabras clave')

        lineas_investigacion = cleaned_data.get('lineas_investigacion')
        if lineas_investigacion.count() == 0:
            raise ValidationError('Debes escoger al menos 1 linea de investigacion')
        
        categoria = cleaned_data.get('categoria')    
        indice_revista = cleaned_data.get('indice_revista')
        if categoria == 'IND' or categoria == 'JCR':
            if not indice_revista: 
                raise ValidationError('Los articulos INDIZADOS o JCR deben tener un indice de revista')
       
        return cleaned_data

class CapituloLibroForm(ModelForm):
    publicacion = forms.DateField(input_formats=['%d-%m-%Y'], required=False)
    # pagina_i
    class Meta:
        model = CapituloLibro
        fields = '__all__'

    def clean(self):

        cleaned_data = super(CapituloLibroForm, self).clean()
        # print(cleaned_data)
        primer_autor = cleaned_data.get('primer_autor')
        primer_coautor = cleaned_data.get('primer_coautor')
        segundo_coautor = cleaned_data.get('segundo_coautor')
        if segundo_coautor:
            if not primer_coautor:
                raise ValidationError('No puedes tener un segundo coautor sin un primer coautor')
                
        if primer_autor == primer_coautor or primer_autor == segundo_coautor or primer_coautor == segundo_coautor:
            raise ValidationError('El autor y los coautores no pueden ser la misma persona')
        
        tipo = cleaned_data.get('tipo')
        pagina_inicio = cleaned_data.get('pagina_inicio')
        pagina_fin = cleaned_data.get('pagina_fin')
        if tipo == 'L':
            if pagina_inicio or pagina_fin:
                raise ValidationError('Un libro no deberia tener pagina de inicio ni de fin')
        else:
            if not pagina_inicio or not pagina_fin:
                raise ValidationError('El capitulo necesita una pagina de inicio y de fin')
            if pagina_fin < pagina_inicio:
                raise ValidationError('La pagina de inicio no puede ser mayor a la pagina de fin')
        
        estado = cleaned_data.get('estado')
        publicacion = cleaned_data.get('publicacion')
        if estado == 'A':
            if publicacion:
                raise ValidationError('No puedes agregar una fecha de publicacion a un articulo no publicado')
        else:
            if not publicacion:
                raise ValidationError('Debes agregar una fecha de publicacion')
                
        palabras_clave = cleaned_data.get('palabras_clave')
        # print(len(palabras_clave))
        # print(palabras_clave.count())
        if palabras_clave.count() < 3:
            raise ValidationError('Debes escoger al menos 3 palabras clave')

        lineas_investigacion = cleaned_data.get('lineas_investigacion')
        if lineas_investigacion.count() == 0:
            raise ValidationError('Debes escoger al menos 1 linea de investigacion')
        
        categoria = cleaned_data.get('categoria')    
        indice_revista = cleaned_data.get('indice_revista')
        if categoria == 'IND' or categoria == 'JCR':
            if not indice_revista: 
                raise ValidationError('Los articulos INDIZADOS o JCR deben tener un indice de revista')
       
        return cleaned_data

class PatenteForm(ModelForm):
    publicacion = forms.DateField(input_formats=['%d-%m-%Y'], required=True)
    class Meta:
        model = Patente
        fields = '__all__'



class CongresoForm(ModelForm):
    class Meta:
        model = Congreso
        fields = '__all__'

class InvestigacionForm(ModelForm):
    class Meta:
        model = Investigacion
        fields = '__all__'

class TesisForm(ModelForm):
    class Meta:
        model = Tesis
        fields = '__all__'
