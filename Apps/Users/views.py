from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

class CustomLogin(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

class Home(TemplateView):
    template_name = 'home.html'

class CustomLogout(LogoutView):
    next_page = 'login'