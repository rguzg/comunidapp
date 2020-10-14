
from django.contrib import admin
from .models import User, Facultad, Nivel, Contrato, LineaInvestigacion, UserActualizado, Alumno, Articulo, Autor, CapituloLibro, Ciudad, Congreso, Contrato, Editorial, Estado, Institucion, Pais, PalabrasClave, Patente, Revista, Tesis
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

UserAdmin.fieldsets = UserAdmin.fieldsets = (         
    (None, {'fields': ('username', 'password')}),         
    (_('Personal info'), {'fields': ('clave', 'first_name', 'last_name', 'email', 'sexo', 'nacimiento', 'foto', 'facultades', 'contratacion', 'grado', 'investigaciones', 'niveles', 'cuerpoAcademico', 'publico', )}),         
    (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    (_('Important dates'), {'fields': ('last_login',)})
)

admin.site.register(User, UserAdmin)
admin.site.register(Facultad)
admin.site.register(Nivel)
admin.site.register(Contrato)
admin.site.register(LineaInvestigacion)
admin.site.register(UserActualizado)
admin.site.register(Alumno)
admin.site.register(Articulo)
admin.site.register(Autor)
admin.site.register(CapituloLibro)
admin.site.register(Ciudad)
admin.site.register(Congreso)
admin.site.register(Editorial)
admin.site.register(Estado)
admin.site.register(Institucion)
admin.site.register(Pais)
admin.site.register(PalabrasClave)
admin.site.register(Patente)
admin.site.register(Revista)
admin.site.register(Tesis)