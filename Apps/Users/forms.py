from django import forms
from django.forms import ModelForm
from .models import Contrato, Facultad, Nivel, LineaInvestigacion, User, Articulo,  CapituloLibro, Patente, Congreso, Investigacion, Tesis, Autor, Revista, Editorial
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

class ArticuloForm(ModelForm):
    class Meta:
        model = Articulo
        fields = '__all__'

class EditorialForm(ModelForm):
    class Meta:
        model = Editorial
        fields = '__all__' 

class CapituloLibroForm(ModelForm):
    class Meta:
        model = CapituloLibro
        fields = '__all__'

class PatenteForm(ModelForm):
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
