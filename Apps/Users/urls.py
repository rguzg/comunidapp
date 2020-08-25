from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.CustomLogin.as_view(), name='login'),
    path('home', login_required(views.Home.as_view()), name='home'),
    path('logout', views.CustomLogout.as_view(), name='logout'),
]
