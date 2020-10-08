from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from .validators import isalphavalidator

def image_user(instance, filename):
    return '{0}/{1}'.format('images_users', instance.username)

def comprobantes(instance, filename):
    return '{0}/{1}'.format('comprobantes', instance.username)

def resumenes(instance, filename):
    return '{0}/{1}'.format('resumenes', instance.username)

grados = [
    ('L', 'Licenciatura'),
    ('M', 'Maestría'),
    ('D', 'Doctorado')
]

estados = [
    ('P', 'Publicado'),
    ('A', 'Aceptado')
]

propositos = [
    ('AT', 'Asimilación tecnológica'),
    ('CT', 'Creación de desarrollo tecnológico'),
    ('DI', 'Difusión'),
    ('GC', 'Generación de conocimiento'),
    ('IA', 'Investigación aplicada'),
    ('TT', 'Transferencia de tecnología')
]

estados = [
    ('P', 'Publicado'),
    ('A', 'Aceptado')
]

propositos = [
    ('AT', 'Asimilación tecnológica'),
    ('CT', 'Creación de desarrollo tecnológico'),
    ('DI', 'Difusión'),
    ('GC', 'Generación de conocimiento'),
    ('IA', 'Investigación aplicada'),
    ('TT', 'Transferencia de tecnología')
]

class User(AbstractUser):
    generos  = [
        ('H', 'Hombre'),
        ('M', 'Mujer')
    ]

    class Meta:
        verbose_name_plural = 'Usuarios'
        ordering = ['id']

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
    estado = models.CharField(max_length=1, null=False, blank=True, choices=estados)
    fecha = models.DateTimeField(auto_now=True, auto_now_add=False)
    motivo = models.CharField(max_length=1000, null=True, blank=True)
    created = models.DateTimeField(auto_now=True, auto_now_add=False)

class Autor(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True, validators=[isalphavalidator])
    last_name = models.CharField(max_length=255, null=True, blank=True, validators=[isalphavalidator])
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        if self.user is None:
            if self.first_name is None or self.last_name is None:
                raise ValidationError('Debes seleccionar un usuario o crear un autor externo con nombre(s) y apellido(s)')

        if len(self.first_name)<=3:
            raise ValidationError('El nombre debe ser mayor a 3 caracteres')

        if len(self.last_name)<=3:
            raise ValidationError('El apellido debe ser mayor a 3 caracteres')

    def __str__(self):
        if self.user is not None:
            if self.user.get_full_name() is "":
                return "{0}".format(self.user.username)
            else:
                return "{0}".format(self.user.get_full_name())
        
        return "{0} {1}".format(self.first_name, self.last_name)
            
class Alumno(models.Model):
    expediente = models.PositiveIntegerField(validators=[
            MaxValueValidator(111111),
            MinValueValidator(999999)
        ])

class PalabrasClave(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False, unique=True)

    def __str__(self):
        return self.nombre

class Pais(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.nombre

class Estado(models.Model):
    nombre = models.CharField(max_length=30)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

class Ciudad(models.Model):
    nombre = models.CharField(max_length=50)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

class Revista(models.Model):
    nombre = models.CharField(max_length=254, null=False, blank=False, unique=True)

    def __str__(self):
        return self.nombre
    
class Editorial(models.Model):
    nombre = models.CharField(max_length=254, null=False, blank=False, unique=True)

    def __str__(self):
        return self.nombre

class Institucion(models.Model):
    nombre = models.CharField(max_length=100)





class Articulo(models.Model):
    categorias = [
        ('ARB', 'Arbitradro'),
        ('IND', 'Indizado'),
        ('JCR', 'Indizado JCR'),
        ('SCP', 'SCOPUS')
    ]

    categoria = models.CharField(max_length=3, choices=categorias, null=False, blank=False)
    primer_autor = models.ForeignKey(Autor, related_name='primer_autor_articulo', on_delete=models.CASCADE, null=False, blank=False)
    primer_colaborador = models.ForeignKey(Autor, related_name='primer_colaborador_articulo',on_delete=models.CASCADE, null=True, blank=True)
    segundo_colaborador = models.ForeignKey(Autor, related_name='segundo_colaborador_articulo',on_delete=models.CASCADE, null=True, blank=True)
    palabras_clave = models.ManyToManyField(PalabrasClave)
    titulo = models.CharField(max_length=300, null=False, blank=False)
    descripcion = models.CharField(max_length=350, null=False, blank=False)
    estado = models.CharField(max_length=1, choices=estados, null=False, blank=False)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    revista = models.ForeignKey(Revista, on_delete=models.CASCADE)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    isnn = models.BigIntegerField()
    publicacion = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    url = models.URLField(max_length=300, null=True, blank=True)
    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()
    volumen = models.PositiveIntegerField(null=True, blank=True)
    lineas_investigacion = models.ManyToManyField(LineaInvestigacion)
    doi = models.URLField(max_length=100, null=True, blank=True)
    indice_revista = models.PositiveIntegerField(null=True, blank=True)

class CapituloLibro(models.Model):
    tipos = [
        ('L', 'Libro'),
        ('C', 'Capitulo')
    ]
    primer_autor = models.ForeignKey(Autor, related_name='primer_autor_capitulo', on_delete=models.CASCADE)
    primer_coautor = models.ForeignKey(Autor, related_name='primer_coautor_libro',on_delete=models.CASCADE)
    segundo_coautor = models.ForeignKey(Autor, related_name='segundo_coautor_libro',on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=tipos)
    titulo = models.CharField(max_length=150)
    palabras_clave = models.ManyToManyField(PalabrasClave)
    estado = models.CharField(max_length=1, choices=estados, null=False, blank=False)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    edicion = models.PositiveIntegerField()
    tiraje = models.PositiveIntegerField()
    isbn = models.CharField(max_length=15)
    publicacion = models.DateField(auto_now=False, auto_now_add=False)
    proposito = models.CharField(max_length=3, choices=propositos)
    lineas_investigacion = models.ManyToManyField(LineaInvestigacion)

class Patente(models.Model):
    autores = models.ManyToManyField(Autor)
    titulo = models.CharField(max_length=300, null=False, blank=False)
    descripcion = models.CharField(max_length=350, null=False, blank=False)
    uso = models.CharField(max_length=255)
    registro = models.CharField(max_length=255)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    publicacion = models.DateField(auto_now=False, auto_now_add=False)
    comprobante = models.FileField(upload_to=comprobantes)
    proposito = models.CharField(max_length=2, choices=propositos)
    lineas_investigacion = models.ManyToManyField(LineaInvestigacion)
    
class Congreso(models.Model):
    primer_autor = models.ForeignKey(Autor, related_name='primer_autor_congreso', on_delete=models.CASCADE)
    primer_colaborador = models.ForeignKey(Autor, related_name='primer_colaborador_congreso',on_delete=models.CASCADE)
    segundo_colaborador = models.ForeignKey(Autor, related_name='segundo_colaborador_congreso',on_delete=models.CASCADE)
    titulo = models.CharField(max_length=300, null=False, blank=False)
    congreso = models.CharField(max_length=300, null=False, blank=False)
    estado = models.CharField(max_length=1, choices=estados, null=False, blank=False)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    publicacion = models.DateField(auto_now=False, auto_now_add=False)
    presentacion = models.DateField(auto_now=False, auto_now_add=False)
    proposito = models.CharField(max_length=2, choices=propositos)
    lineas_investigacion = models.ManyToManyField(LineaInvestigacion)
    palabras_clave = models.ManyToManyField(PalabrasClave)

class Investigacion(models.Model):

    tipos_financiamiento = [
        ('I', 'Interno'),
        ('E', 'Externo')
    ]
    tipos_proyecto = [
        ('I','Investigación'),
        ('V', 'Vinculación')
    ]
    tipo_proyecto = models.CharField(max_length=1, choices=tipos_proyecto)
    titulo = models.CharField(max_length=300, null=False, blank=False)
    financiamiento = models.BooleanField(null=False, blank=False)
    tipo_financiamiento = models.CharField(max_length=1, choices=tipos_financiamiento, null=True, blank=True)
    inicio = models.DateField(auto_now=False, auto_now_add=False)
    fin = models.DateField(auto_now=False, auto_now_add=False)
    responsable = models.ForeignKey(Autor, related_name='responsable_investigacion', on_delete=models.CASCADE)
    primer_colaborador = models.ForeignKey(Autor, related_name='primer_colaborador_investigacion',on_delete=models.CASCADE)
    segundo_colaborador = models.ForeignKey(Autor, related_name='segundo_colaborador_investigacion',on_delete=models.CASCADE)
    primer_alumno = models.ForeignKey(Alumno, related_name='primer_alumno_investigacion', on_delete=models.CASCADE)
    segundo_alumno = models.ForeignKey(Alumno, related_name='segundo_alumno_investigacion', on_delete=models.CASCADE)
    tercer_alumno = models.ForeignKey(Alumno,related_name='tercer_alumno_investigacion', on_delete=models.CASCADE)
    resumen = models.FileField(upload_to=resumenes)
    palabras_clave = models.ManyToManyField(PalabrasClave)
    lineas_investigacion = models.ManyToManyField(LineaInvestigacion)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)

class Tesis(models.Model):
    titulo = models.CharField(max_length=300, null=False, blank=False)
    grado = models.CharField(max_length=1, choices=grados)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    inicio = models.DateField(auto_now=False, auto_now_add=False)
    fin = models.DateField(auto_now=False, auto_now_add=False)
    profesor = models.ForeignKey(User, on_delete=models.CASCADE)
    lineas_investigacion = models.ManyToManyField(LineaInvestigacion)