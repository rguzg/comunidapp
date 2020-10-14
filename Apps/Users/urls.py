from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required, user_passes_test
from . import views

urlpatterns = [
    # path('paises', views.paises, name='paises'),

    # URLS para el funcionamiento de los usuarios
    path('', views.CustomLogin.as_view(), name='login'),
    path('logout', login_required(views.CustomLogout.as_view()), name='logout'),
    path('home', login_required(views.Home.as_view()), name='home'),
    path('profile', login_required(views.Profile.as_view()), name='profile'),
    path('password', login_required(views.CustomResetPassword.as_view()), name="password"),
    path('<slug:pk>/', login_required(views.Perfil.as_view()), name='profile-detail'),

    #URLS para el uso del usuario Administrador
    path('updates', user_passes_test(lambda u: u.is_superuser, redirect_field_name='home')(views.UpdatedUsers.as_view()), name='updates'),
    
    #URLS para agregar nuevos productos
    path('new/articulo', login_required(views.AddArticulo.as_view()), name="AddArticulo"),
    path('new/libro', login_required(views.AddCapituloLibro.as_view()), name="AddCapituloLibro"),
    path('new/patente', login_required(views.AddPatente.as_view()), name="AddPatente"),
    path('new/congreso', login_required(views.AddCongreso.as_view()), name="AddCongreso"),
    path('new/investigacion', login_required(views.AddInvestigacion.as_view()), name="AddInvestigacion"),
    path('new/tesis', login_required(views.AddTesis.as_view()), name="AddTesis"),

    #URLs para agregar campos foraneos de nuevos productos
    url(r'^author/create', login_required(views.AutorCreatePopup.as_view()), name = "AuthorCreate"),
    url(r'^revista/create', login_required(views.RevistaCreatePopup.as_view()), name = "RevistaCreate"),
    url(r'^editorial/create', login_required(views.EditorialCreatePopup.as_view()), name = "EditorialCreate"),
    url(r'^palabras/create', login_required(views.PalabrasCreatePopup.as_view()), name = "PalabrasCreate"),
    url(r'^lineas/create', login_required(views.LineasCreatePopup.as_view()), name = "LineasCreate"),
    url(r'^alumno/create', login_required(views.AlumnoCreatePopup.as_view()), name = "AlumnoCreate"),
    url(r'^institucion/create', login_required(views.InstitucionCreatePopup.as_view()), name = "InstitucionCreate"),
]
