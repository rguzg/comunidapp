from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required, user_passes_test
# from django.views.decorators.csrf import csrf_exempt
from . import views, views_busqueda, views_serializer, view_proxy, views_relaciones

urlpatterns = [
    # URLS para el uso de los usuarios normales
    path('', views.CustomLogin.as_view(), name='login'),
    path('searchUsers', views.SearchUsers.as_view(), name='searchUsers'),
    path('getProducto', views.getProducto.as_view(), name='getProducto'),
    path('logout', login_required(views.CustomLogout.as_view()), name='logout'),
    path('home', login_required(views.Home.as_view()), name='home'),
    path('profile', login_required(views.Profile.as_view()), name='profile'),
    path('password', login_required(views.CustomResetPassword.as_view()), name="password"),
    path('user/<slug:pk>/', login_required(views.Perfil.as_view()), name='profile-detail'),
    
    #URLS para el uso del usuario Administrador
    path('updates', user_passes_test(lambda u: u.is_superuser, redirect_field_name='home')(views.UpdatedUsers.as_view()), name='updates'),
    path('add/admin', user_passes_test(lambda u: u.is_superuser, redirect_field_name='home')(views.AddAdminUsers.as_view()), name='AddAdminUsers'),
    path('add/profesor', user_passes_test(lambda u: u.is_superuser, redirect_field_name='home')(views.AddProfesorUsers.as_view()), name='AddProfesorUsers'),
    path('profileAdmin', user_passes_test(lambda u: u.is_superuser, redirect_field_name='home')(views.Profile_Admin.as_view()), name='profileAdmin'),
    
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
    url(r'^facultad/create', login_required(views.FacultadCreatePopup.as_view()), name = "FacultadCreate"),
    url(r'^nivel/create', login_required(views.NivelesCreatePopup.as_view()), name = "NivelCreate"),
    url(r'^contrato/create', login_required(views.ContratoCreatePopup.as_view()), name = "ContratoCreate"),
    url(r'^estadoP/create', login_required(views.EstadoPCreatePopup.as_view()),
        name="EstadoPCreate"),
    url(r'^ciudad/create', login_required(views.CiudadCreatePopup.as_view()),
        name="CiudadCreate"),

    #URLs para realizar busquedas
    path('buscar/lineas', login_required(views_busqueda.BuscarLineas.as_view()), name="BuscarLineas"),
    path('buscar/facultades', login_required(views_busqueda.BuscarFacultades.as_view()), name="BuscarFacultades"),
    path('buscar/niveles', login_required(views_busqueda.BuscarNiveles.as_view()), name="BuscarNiveles"),
    path('buscar/palabras', login_required(views_busqueda.BuscarPalabrasClave.as_view()), name="BuscarPalabrasClave"),

    #URLs de Serializers
    path('api/lineas', views_serializer.LineasInvestigacion_Serializer_View.as_view(), name="API_Lineas"),
    path('api/facultades', views_serializer.Facultad_Serializer_View.as_view(), name="API_Facultades"),
    path('api/niveles', views_serializer.Nivel_Serializer_View.as_view(), name="API_Niveles"),
    path('api/palabras', views_serializer.PalabraClave_Serializer_View.as_view(), name="API_PalabrasClave"),

    #URLs de preprocesamiento de forms
    path('proxy', view_proxy.Proxy.as_view(), name="FormPerfil"),

    #URL de relaciones
    path('generarRelaciones', user_passes_test(lambda u: u.is_superuser, redirect_field_name='home')(views.GenerarRelaciones.as_view()), name = 'Generar_Relaciones'),
    # Los productos que generan tienen relaciones son: articulos, capitulolibros, patentes, congresos, investigaciones
    path('relaciones/<str:producto>/', views_relaciones.Relaciones.as_view(), name='relaciones_investigaciones'),
    path('visualization', user_passes_test(lambda u: u.is_superuser, redirect_field_name='home')(views_relaciones.Visualization.as_view()), name='visualization'),
    path('visualization-full', user_passes_test(lambda u: u.is_superuser, redirect_field_name='home')(views_relaciones.VisualizationFull.as_view()), name='visualization-full'),
]
