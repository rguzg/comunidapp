from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import Contrato, Facultad, Nivel, LineaInvestigacion, User
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


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
