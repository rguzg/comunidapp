from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from .forms import UserForm
from .models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


class CustomLogin(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


class Home(TemplateView):
    template_name = 'home.html'


class Profile(UpdateView):
    model = User
    fields = ['clave', 'first_name', 'last_name', 'email', 'sexo', 'nacimiento',
              'foto',  'contratacion', 'grado', 'facultades', 'niveles', 'investigaciones']
    template_name = 'my_profile.html'
    template_name_suffix = '_update_form'
    success_url = "/profile/1"


class CustomLogout(LogoutView):
    next_page = 'login'


def CustomResetPassword(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Contraseña cambiada correctamente')
            return render(request, 'password.html', {
                'form': form
            })
        else:
            return render(request, 'password.html', {
                'form': form
            })
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'password.html', {
            'form': form,
        })
