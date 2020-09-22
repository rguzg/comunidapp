
from django.contrib import admin
from .models import User, Facultad, Nivel, Contrato, LineaInvestigacion, UserActualizado
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

UserAdmin.fieldsets = UserAdmin.fieldsets = (         
    (None, {'fields': ('username', 'password')}),         
    (_('Personal info'), {'fields': ('clave', 'first_name', 'last_name', 'email', 'sexo', 'nacimiento', 'foto', 'facultades', 'contratacion', 'grado', 'investigaciones', 'niveles')}),         
    (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    (_('Important dates'), {'fields': ('last_login',)})
)
admin.site.register(User, UserAdmin)
admin.site.register(Facultad)
admin.site.register(Nivel)
admin.site.register(Contrato)
admin.site.register(LineaInvestigacion)
admin.site.register(UserActualizado)