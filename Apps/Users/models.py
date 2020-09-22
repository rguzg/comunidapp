from django.db import models
from django.contrib.auth.models import AbstractUser

# CUERPO ACADEMICO: FK - 18 DIGITOS LETRAS Y NUMEROS, INACTIVO/ACTIVO, PUBLICO/PRIVADO

def image_user(instance, filename):
    return '{0}/{1}'.format('images_users', instance.username)

class User(AbstractUser):
    generos  = [
        ('H', 'Hombre'),
        ('M', 'Mujer')
    ]

    grados = [
        ('L', 'Licenciatura'),
        ('M', 'Maestría'),
        ('D', 'Doctorado')
    ]

    class Meta:
        verbose_name_plural = 'Usuarios'

    email = models.EmailField(unique=True, blank=True, null=True)
    clave = models.PositiveIntegerField(unique=True, blank=False, null=True, verbose_name = 'Clave de empleado')
    sexo = models.CharField(max_length=1, choices=generos, blank=False, null=True, verbose_name = 'Genero')
    nacimiento = models.DateField(auto_now=False, auto_now_add=False, blank=False, null=True, verbose_name = 'Fecha de nacimiento')
    foto = models.ImageField(upload_to=image_user)
    grado =  models.CharField(max_length=1, choices=grados, blank=False, null=True, verbose_name = 'Último grado de estudios')
    cuerpoAcademico = models.CharField(max_length=18, blank=False, null=True, verbose_name='Cuerpo Académico')
    publico = models.BooleanField(default=False)
    contratacion = models.ForeignKey('Contrato', on_delete=models.CASCADE, blank=False, null=True, verbose_name = 'Tipo de contrato')
    facultades = models.ManyToManyField('Facultad', verbose_name = 'Facultades donde imparte clases')
    niveles = models.ManyToManyField('Nivel', verbose_name= 'Niveles donde imparte clases')
    investigaciones = models.ManyToManyField('LineaInvestigacion', verbose_name= 'Lineas de investigación o áreas de interes')

# Facultad en la cual labora
class Facultad(models.Model):
    nombre = models.CharField(max_length=70, unique=True, blank=False, null=False)

    class Meta:
        verbose_name_plural = 'Facultades'

    def __str__(self):
        return self.nombre

# Nivel en los cuales imparte clases (Licenciatura, Maestria y Doctorado)
class Nivel(models.Model):
    nombre = models.CharField(max_length=254, unique=True, blank=False, null=False)

    class Meta:
        verbose_name_plural = 'Niveles de Clases Impartidas'

    def __str__(self):
        return self.nombre

# Tipo de contrato que sostiene con la universidad (Honorarios, Tiempo Libre o Tiempo Completo)
class Contrato(models.Model):
    tipo = models.CharField(max_length=50, unique=True, blank=False, null=False)

    class Meta:
        verbose_name_plural = 'Tipos de Contrato'

    def __str__(self):
        return self.tipo

# Lineas de investigacion e interes del maestro
class LineaInvestigacion(models.Model):

    nombre = models.CharField(max_length=100, unique=True, blank=False, null=False)

    class Meta:
        verbose_name_plural = 'Lineas de Investigación'

    def __str__(self):
        return self.nombre

class UserActualizado(models.Model):

    class Meta:
        ordering=['-id']
        
    estados  = [
        ('P', 'Pendiente'),
        ('A', 'Aprobado'),
        ('R', 'Rechazado')
    ]

    user = models.OneToOneField('User', on_delete=models.CASCADE)
    cambios = models.CharField(max_length=1000, null=True, blank=True)
    estado = models.CharField(max_length=1, null=False, blank=True, choices=estados, default='P')
    fecha = models.DateTimeField(auto_now=True, auto_now_add=False)
    motivo = models.CharField(max_length=1000, null=True, blank=True)