from django.core.validators import RegexValidator

'''
This regex assumes that you have a clean string,
you should clean the string for spaces and other characters
'''

isalphavalidator = RegexValidator(r'^[a-zA-Z ]+$',
                             message='El nombre debe ser alfanumerico',
                             code='Nombre no válido')