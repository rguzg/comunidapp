from django.core.validators import RegexValidator
from django import template
register = template.Library()
from django.core.exceptions import ValidationError

isalphavalidator = RegexValidator(r'^[a-zA-Z ]+$',
                             message='El nombre debe ser alfanumerico',
                             code='Nombre no válido')

def validate_file_size(value):
    filesize= value.size
    if filesize > 26214400:
        raise ValidationError("El tamaño máximo del archivo que se puede subir son 25MB")
    else:
        return value
