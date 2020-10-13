from django.core.validators import RegexValidator
from django import template
register = template.Library()

isalphavalidator = RegexValidator(r'^[a-zA-Z ]+$',
                             message='El nombre debe ser alfanumerico',
                             code='Nombre no válido')
  
