from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from .validators import isalphavalidator, validate_file_size
from django.core.validators import FileExtensionValidator
from cloudinary_storage.storage import MediaCloudinaryStorage

"""
Modelo del usuario
"""
grados = [
    ('L', 'Licenciatura'),
    ('M', 'Maestría'),
    ('D', 'Doctorado')
]

generos  = [
        ('H', 'Hombre'),
        ('M', 'Mujer')
    ]

def image_user(instance, filename):
    return '{0}/{1}'.format('images_users', instance.username)

def temp_image_user(instance, filename):
    return '{0}/{1}'.format('images_users', instance.username)

class User(AbstractUser):

    class Meta:
        verbose_name_plural = 'Usuarios'
        ordering = ['id']
    email = models.EmailField(unique=True, blank=True, null=True)
    clave = models.PositiveIntegerField(unique=True, blank=False, null=True, verbose_name = 'Clave de empleado', validators=[
            MaxValueValidator(999999),
            MinValueValidator(1)
        ])
    sexo = models.CharField(max_length=1, choices=generos, blank=False, null=True, verbose_name = 'Genero')
    nacimiento = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name = 'Fecha de nacimiento')
    foto = models.ImageField(null=True, blank=True, upload_to=image_user, storage=MediaCloudinaryStorage())
    grado =  models.CharField(max_length=1, choices=grados, blank=False, null=True, verbose_name = 'Último grado de estudios')
    cuerpoAcademico = models.CharField(max_length=18, blank=False, null=True, verbose_name='Cuerpo Académico')
    publico = models.BooleanField(default=False)
    contratacion = models.ForeignKey('Contrato', on_delete=models.CASCADE, blank=False, null=True, verbose_name = 'Tipo de contrato')
    facultades = models.ManyToManyField('Facultad', verbose_name = 'Facultades donde imparte clases')
    niveles = models.ManyToManyField('Nivel', verbose_name= 'Niveles donde imparte clases')
    investigaciones = models.ManyToManyField('LineaInvestigacion', verbose_name= 'Lineas de investigación o áreas de interes')

    def __unicode__(self):
        try:
            foto_id = self.foto.id
        except AttributeError:
            foto_id = ''
        return "Foto <%s:%s>" % (self.email, foto_id)

class UpdateRequest(models.Model):
    class Meta:
        ordering=['-fecha']
        
    estados  = [
        ('P', 'Pendiente'),
        ('A', 'Aprobado'),
        ('R', 'Rechazado')
    ]
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    estado = models.CharField(max_length=1, null=True, blank=False, choices=estados)
    fecha = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name = 'Fecha')
    motivo = models.CharField(max_length=1000, null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=False)
    last_name = models.CharField(max_length=150, null=True, blank=False)
    email = models.EmailField(null=True, blank=False)
    clave = models.PositiveIntegerField(null=True, blank=False, 
        verbose_name = 'Clave de empleado', 
        validators=[
            MaxValueValidator(999999),
            MinValueValidator(1)
        ])
    sexo = models.CharField(max_length=1, choices=generos, blank=False, null=True, verbose_name = 'Genero')
    nacimiento = models.DateField(auto_now=False, auto_now_add=False, blank=False, null=True, verbose_name = 'Fecha de nacimiento')
    foto = models.ImageField(upload_to=temp_image_user, null=True, blank=True, storage=MediaCloudinaryStorage())
    grado =  models.CharField(max_length=1, choices=grados, blank=False, null=True, verbose_name = 'Último grado de estudios')
    cuerpoAcademico = models.CharField(max_length=18, blank=False, null=True, verbose_name='Cuerpo Académico')
    publico = models.BooleanField(null=True, blank=False)
    contratacion = models.ForeignKey('Contrato', on_delete=models.CASCADE, blank=False, null=True, verbose_name = 'Tipo de contrato')
    facultades = models.ManyToManyField('Facultad',  blank=True, verbose_name = 'Facultades donde imparte clases')
    niveles = models.ManyToManyField('Nivel', blank=True, verbose_name= 'Niveles donde imparte clases')
    investigaciones = models.ManyToManyField('LineaInvestigacion', blank=True, verbose_name= 'Lineas de investigación o áreas de interes')
    changed_fields = models.JSONField(null=True, blank=True)

"""
Modelos auxiliares o de llaves foraneas
"""
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

# Facultad en la cual labora
class Facultad(models.Model):
    nombre = models.CharField(max_length=70, unique=True, blank=False, null=False)

    class Meta:
        verbose_name = 'Facultad'
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

class Autor(models.Model):

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

    first_name = models.CharField(max_length=255, null=True, blank=True, validators=[isalphavalidator])
    last_name = models.CharField(max_length=255, null=True, blank=True, validators=[isalphavalidator])
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    

    def __str__(self):
        if self.user is not None:
            if self.user.get_full_name() is "":
                return "{0}".format(self.user.username)
            else:
                return "{0}".format(self.user.get_full_name())
        
        return "{0} {1}".format(self.first_name, self.last_name)
            
class Alumno(models.Model):

    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'

    expediente = models.PositiveIntegerField(unique=True, validators=[
            MaxValueValidator(999999),
            MinValueValidator(111111)
        ])

    def __str__(self):
        return "{0}".format(self.expediente)

class PalabrasClave(models.Model):

    class Meta:
        verbose_name = 'Palabra clave'
        verbose_name_plural = ' Palabras clave'

    nombre = models.CharField(max_length=50, null=False, blank=False, unique=True)

    def __str__(self):
        return self.nombre

class Pais(models.Model):
    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'

    nombre = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.nombre

class Estado(models.Model):
    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
    nombre = models.CharField(max_length=30)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'

    nombre = models.CharField(max_length=50)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

class Revista(models.Model):
    class Meta:
        verbose_name = 'Revista'
        verbose_name_plural = 'Revistas'

    nombre = models.CharField(max_length=254, null=False, blank=False, unique=True)

    def __str__(self):
        return self.nombre
    
class Editorial(models.Model):
    class Meta:
        verbose_name = 'Editorial'
        verbose_name_plural = 'Editoriales'

    nombre = models.CharField(max_length=254, null=False, blank=False, unique=True)

    def __str__(self):
        return self.nombre

class Institucion(models.Model):
    class Meta:
        verbose_name = 'Institución'
        verbose_name_plural = 'Instituciones'
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


"""
Modelos principales
"""
def comprobantes(instance, filename):
    return '{0}/{1}.{2}'.format('comprobantes', instance.registro, 'pdf')

def resumenes(instance, filename):
    return '{0}/{1}.{2}'.format('resumenes', instance.titulo, 'pdf')

class Articulo(models.Model):
    class Meta:
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'

    categorias = [
        ('ARB', 'Arbitrado'),
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
    url = models.URLField(max_length=300, null=False, blank=False)
    pagina_inicio = models.PositiveIntegerField()
    pagina_fin = models.PositiveIntegerField()
    volumen = models.PositiveIntegerField(null=True, blank=True)
    lineas_investigacion = models.ManyToManyField(LineaInvestigacion)
    doi = models.URLField(max_length=100, null=False, blank=False)
    indice_revista = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return 'Articulo: "{0}" '.format(self.titulo)

class CapituloLibro(models.Model):
    
    class Meta:
        verbose_name = 'Libro/Capítulo'
        verbose_name_plural = 'Libros/Capítulo'

    tipos = [
        ('L', 'Libro'),
        ('C', 'Capitulo')
    ]
    primer_autor = models.ForeignKey(Autor, related_name='primer_autor_capitulo', on_delete=models.CASCADE)
    primer_coautor = models.ForeignKey(Autor, related_name='primer_coautor_libro',on_delete=models.CASCADE, null=True, blank=True)
    segundo_coautor = models.ForeignKey(Autor, related_name='segundo_coautor_libro',on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=1, choices=tipos)
    titulo = models.CharField(max_length=150)
    pagina_inicio = models.PositiveIntegerField(null=True, blank=True)
    pagina_fin = models.PositiveIntegerField(null=True, blank=True)
    palabras_clave = models.ManyToManyField(PalabrasClave)
    estado = models.CharField(max_length=1, choices=estados, null=False, blank=False)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    edicion = models.PositiveIntegerField()
    tiraje = models.PositiveIntegerField()
    isbn = models.CharField(max_length=15)
    publicacion = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    proposito = models.CharField(max_length=3, choices=propositos)
    lineas_investigacion = models.ManyToManyField(LineaInvestigacion)

    def __str__(self):
        if self.tipo == 'L':
            return 'Libro: {0}'.format(self.titulo)
        else:
            return 'Capitulo: {0}'.format(self.titulo)

class Patente(models.Model):

    class Meta:
        verbose_name = 'Patente'
        verbose_name_plural = 'Patentes'

    autores = models.ManyToManyField(Autor)
    titulo = models.CharField(max_length=300, null=False, blank=False)
    descripcion = models.CharField(max_length=350, null=False, blank=False)
    uso = models.CharField(max_length=255)
    registro = models.CharField(max_length=25)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    publicacion = models.DateField(auto_now=False, auto_now_add=False)
    comprobante = models.FileField(upload_to=comprobantes, validators=[FileExtensionValidator(allowed_extensions=['PDF']), validate_file_size])
    proposito = models.CharField(max_length=2, choices=propositos)
    lineas_investigacion = models.ManyToManyField(LineaInvestigacion)

class Congreso(models.Model):
    class Meta:
        verbose_name = 'Congreso'
        verbose_name_plural = 'Congresos'

    primer_autor = models.ForeignKey(Autor, related_name='primer_autor_congreso', on_delete=models.CASCADE)
    primer_colaborador = models.ForeignKey(Autor, related_name='primer_colaborador_congreso',on_delete=models.CASCADE, null=True, blank=True)
    segundo_colaborador = models.ForeignKey(Autor, related_name='segundo_colaborador_congreso',on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(max_length=300, null=False, blank=False)
    congreso = models.CharField(max_length=300, null=False, blank=False)
    estado = models.CharField(max_length=1, choices=estados, null=False, blank=False)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    estadoP = models.ForeignKey(Estado, on_delete=models.CASCADE, null=True, blank=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, null=True, blank=True)
    publicacion = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    presentacion = models.DateField(auto_now=False, auto_now_add=False)
    proposito = models.CharField(max_length=2, choices=propositos)
    lineas_investigacion = models.ManyToManyField(LineaInvestigacion)
    palabras_clave = models.ManyToManyField(PalabrasClave)

class Investigacion(models.Model):
    class Meta:
        verbose_name = 'Investigación'
        verbose_name_plural = 'Investigaciones'

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
    primer_colaborador = models.ForeignKey(Autor, related_name='primer_colaborador_investigacion',on_delete=models.CASCADE, null=True, blank=True)
    segundo_colaborador = models.ForeignKey(Autor, related_name='segundo_colaborador_investigacion',on_delete=models.CASCADE, null=True, blank=True)
    primer_alumno = models.ForeignKey(Alumno, related_name='primer_alumno_investigacion', on_delete=models.CASCADE, null=True, blank=True)
    segundo_alumno = models.ForeignKey(Alumno, related_name='segundo_alumno_investigacion', on_delete=models.CASCADE, null=True, blank=True)
    tercer_alumno = models.ForeignKey(Alumno,related_name='tercer_alumno_investigacion', on_delete=models.CASCADE, null=True, blank=True)
    resumen = models.FileField(upload_to=resumenes, validators=[FileExtensionValidator(allowed_extensions=['PDF'])])
    palabras_clave = models.ManyToManyField(PalabrasClave)
    lineas_investigacion = models.ManyToManyField(LineaInvestigacion)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)

class Tesis(models.Model):
    
    class Meta:
        verbose_name = 'Tesis'
        verbose_name_plural = 'Tesis'

    titulo = models.CharField(max_length=300, null=False, blank=False)
    grado = models.CharField(max_length=1, choices=grados)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    inicio = models.DateField(auto_now=False, auto_now_add=False)
    fin = models.DateField(auto_now=False, auto_now_add=False)
    profesor = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=True)
    lineas_investigacion = models.ManyToManyField(LineaInvestigacion)
    palabras_clave = models.ManyToManyField(PalabrasClave)