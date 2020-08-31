from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.CustomLogin.as_view(), name='login'),
    path('home', login_required(views.Home.as_view()), name='home'),
    path('profile/<slug:pk>', login_required(views.Profile.as_view()), name='profile'),
    path('logout', login_required(views.CustomLogout.as_view()), name='logout'),
    path('password', login_required(views.CustomResetPassword), name="password"),
]
