from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required, user_passes_test
from . import views

urlpatterns = [
    # path('paises', views.paises, name='paises'),
    path('', views.CustomLogin.as_view(), name='login'),
    path('logout', login_required(views.CustomLogout.as_view()), name='logout'),
    path('home', login_required(views.Home.as_view()), name='home'),
    path('profile', login_required(views.Profile.as_view()), name='profile'),
    path('updates', user_passes_test(lambda u: u.is_superuser, redirect_field_name='home')(views.UpdatedUsers.as_view()), name='updates'),
    path('password', login_required(views.CustomResetPassword.as_view()), name="password"),
    path('add-product', login_required(views.AddProduct.as_view()), name="add-product"),
    path('<slug:pk>/', login_required(views.Perfil.as_view()), name='profile-detail'),
    url(r'^author/create', views.AutorCreatePopup.as_view(), name = "AuthorCreate"),
    url(r'^revista/create', views.RevistaCreatePopup.as_view(), name = "RevistaCreate"),
    url(r'^editorial/create', views.EditorialCreatePopup.as_view(), name = "EditorialCreate"),
    url(r'^palabras/create', views.PalabrasCreatePopup.as_view(), name = "PalabrasCreate"),
]
