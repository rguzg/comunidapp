import ast
import json
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponse, redirect, render
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormView, UpdateView
from .forms import (AlumnoForm, ArticuloForm, AuthenticationForm, AutorForm,
                    CapituloLibroForm, CongresoForm, EditorialForm,
                    InstitucionForm, InvestigacionForm, LineasForm,
                    PalabrasForm, PatenteForm, RevistaForm, TesisForm,
                    UserActualizadoForm)
from .models import (Articulo, Contrato, Facultad, LineaInvestigacion, Nivel,
                     Pais, User, UserActualizado)

"""
Clases para el manejo y administracion de sesiones y de usuarios
"""
# CBV para el Login (necesario LOGIN_URL, LOGIN_REDIRECT_URL y LOGOUT_REDIRECT_URL en SETTINGS)
class CustomLogin(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    authentication_form = AuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inicia sesión en Comunidapp'
        return context

# CBV para el HTML de Home (donde se listan los usuarios)
class Home(ListView):
    template_name = 'home.html'
    paginate_by = 20
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Comunidapp'
        return context

    # def get_queryset(self):
    #     queryset = User.objects.filter(is_superuser=False)
    #     return queryset

# CBV para el perfil detallado de cada usuario
class Perfil(DetailView):
    model = User
    template_name = 'perfil-detail.html'

    def get_context_data(self, **kwargs):
        context = super(Perfil, self).get_context_data(**kwargs)
        user = super().get_object()
        context['title'] = "Perfil de {0}".format(user.get_full_name())
        return context

# CBV para actualizar los datos del perfil del usuario
class Profile(FormView):
    form_class = UserActualizadoForm
    template_name = 'my_profile.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['title'] = "Actualización de mis datos"
        return context

    def form_valid(self, form):
        """
        Funcion que detecta que campos cambiaron y guarda unicamente los cambiados
        """
        data = {}
        if form.has_changed():
            for field in form.changed_data:
                data[field] = str(form.cleaned_data[field])

        print(data)
        update, created = UserActualizado.objects.get_or_create(
            user=self.request.user)
        if(update.estado == 'P'):
            form.add_error(
                None, 'Ya cuentas con una peticion de actualización. Espera a que se apruebe o rechace.')
            return super().form_invalid(form)

        update.cambios = data
        update.estado = 'P'
        update.save()
        return super().form_valid(form)

    def get_initial(self):
        """
        Regresando la informacion del usuario al formulario,
        ya que no es un ModelForm
        """
        initial = super().get_initial()
        initial['email'] = self.request.user.email
        initial['clave'] = self.request.user.clave
        initial['sexo'] = self.request.user.sexo
        initial['nacimiento'] = self.request.user.nacimiento
        initial['foto'] = self.request.user.foto
        initial['grado'] = self.request.user.grado
        initial['contratacion'] = self.request.user.contratacion
        initial['niveles'] = [
            nivel for nivel in Nivel.objects.all().values_list('id', flat=True)]
        initial['facultades'] = [
            facu for facu in Facultad.objects.all().values_list('id', flat=True)]
        initial['investigaciones'] = [
            inve for inve in LineaInvestigacion.objects.all().values_list('id', flat=True)]
        return initial

# CBV para la funcionalidad de Logout
class CustomLogout(LogoutView):
    next_page = 'login'

# CBV para la funcionalidad de cambiar la contraseña
class CustomResetPassword(View):
    form_class = PasswordChangeForm
    template_name = 'password.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(
            user=request.user
        )
        return render(request, 'password.html', {
            'form': form,
            'title': 'Cambio de contraseña'
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Contraseña cambiada correctamente')

        return render(request, 'password.html', {
            'form': form,
            'title': 'Cambio de contraseña'
        })

# CBV para aprobar o rechazar peticion de actualizaciones de perfil
class UpdatedUsers(ListView):
    model = UserActualizado
    paginate_by = 10
    template_name = 'updates.html'
    ordering = ['-created']

    def get_queryset(self):
        return UserActualizado.objects.filter(estado='P')

    def post(self, request, *args, **kwargs):
        idUserActualizado = request.POST['id']
        query = UserActualizado.objects.get(id=idUserActualizado)
        cambios = query.cambios.replace("\'", "\"")
        cambios = json.loads(cambios)

        user = User.objects.get(id=query.user.id)

        for attr, value in cambios.items():
            if attr == 'contratacion':
                value = Contrato.objects.get(tipo=value)
            # if attr == 'facultades':
            # if attr == 'niveles':
            #     print("si")
            #     # user.niveles.clear()
            #     print(*value)
            #     print(ast.literal_eval(value))
            #     user.niveles.add(*value)

            # if value == 'investigaciones':
            setattr(user, attr, value)
            # print(attr, ': ', value)
        user.save()

        query.estado = 'A'
        query.cambios = '{}'
        query.save()

        return redirect('updates')

    def get_context_data(self, **kwargs):
        context = super(UpdatedUsers, self).get_context_data(**kwargs)
        context['title'] = 'Peticiones de actualización'
        # import ast
        # print(ast.literal_eval("{'email': 'email@gmail.com2', 'clave': 2, 'sexo': 'H'}"))
        return context
        


"""
Clases para agregar productos
"""
class AddArticulo(SuccessMessageMixin, CreateView):
    template_name = 'add-producto.html'
    form_class = ArticuloForm
    success_url = '/new/articulo'
    success_message = 'Artículo creado correctamente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agrega un artículo'
        return context

class AddCapituloLibro(SuccessMessageMixin, CreateView):
    template_name = 'add-producto.html'
    form_class = CapituloLibroForm
    success_url = '/new/libro'
    success_message = 'Libro/Capítulo creado correctamente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agrega un libro o capítulo'
        return context

class AddPatente(SuccessMessageMixin, CreateView):
    template_name = 'add-producto.html'
    form_class = PatenteForm
    success_url = '/new/patente'
    success_message = 'Patente creada correctamente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agrega una patente'
        return context

class AddCongreso(SuccessMessageMixin, CreateView):
    template_name = 'add-producto.html'
    form_class = CongresoForm
    success_url = '/new/congreso'
    success_message = 'Participacion en congreso creada correctamente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agrega un partición en congreso'
        return context

class AddInvestigacion(SuccessMessageMixin, CreateView):
    template_name = 'add-producto.html'
    form_class = InvestigacionForm
    success_url = '/new/investigacion'
    success_message = 'Proyecto de Investigacion/Vinculacion agregado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agrega un proyecto de investigación'
        return context

class AddTesis(SuccessMessageMixin, CreateView):
    template_name = 'add-producto.html'
    form_class = TesisForm
    success_url = '/new/tesis'
    success_message = 'Dirección de tesis agregada'

    def get_initial(self):
        initial = super(AddTesis, self).get_initial()
        initial = initial.copy()
        initial['profesor'] = self.request.user
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super(AddTesis, self).get_context_data(*args,**kwargs)
        context['title'] = 'Agrega una dirección de tesis'
        return context


"""
Clases para la creacion de campos foraneos (aparecen como PopUp)
"""
class AutorCreatePopup(View):
    def get(self, request, *args, **kwargs):
        form = AutorForm()
        return render(request, 'add-externo.html', {
            'form': form,
            'title': 'Agrega un Autor o Colaborador externo'
            })

    def post(self, request, *args, **kwargs):
        form = AutorForm(request.POST)
        if form.is_valid():
            id_field = form.cleaned_data.get('id_field')
            print(id_field)
            instance = form.save()
            return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "%s");</script>' % (instance.pk, instance, id_field))
        return render(request, 'add-externo.html', {
            'form': form,
            'title': 'Agrega un Autor/Colaborador externo'
        })

class AlumnoCreatePopup(View):
    def get(self, request, *args, **kwargs):
        form = AlumnoForm()
        return render(request, 'add-externo.html', {
            'form': form, 
            'title': 'Agrega un Alumno'
            })

    def post(self, request, *args, **kwargs):
        form = AlumnoForm(request.POST)
        if form.is_valid():
            id_field = form.cleaned_data.get('id_field')
            print(id_field)
            instance = form.save()
            return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "%s");</script>' % (instance.pk, instance, id_field))
        return render(request, 'add-externo.html', {
            'form': form, 
            'title': 'Agrega un Alumno'
            })

class RevistaCreatePopup(View):
    def get(self, request, *args, **kwargs):
        form = RevistaForm()
        return render(request, "add-externo.html", {
            "form": form, 
            'title': 'Agrega una Revista'
            })

    def post(self, request, *args, **kwargs):
        form = RevistaForm(request.POST)
        if form.is_valid():
            id_field = form.cleaned_data.get('id_field')
            print(id_field)
            instance = form.save()
            return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "%s");</script>' % (instance.pk, instance, id_field))
        return render(request, "add-externo.html", {
            "form": form, 
            'title': 'Agrega una Revista'
            })

class EditorialCreatePopup(View):
    def get(self, request, *args, **kwargs):
        form = EditorialForm()
        return render(request, "add-externo.html", {
            "form": form, 
            'title': 'Agrega una Editorial'
            })

    def post(self, request, *args, **kwargs):
        form = EditorialForm(request.POST)
        if form.is_valid():
            id_field = form.cleaned_data.get('id_field')
            print(id_field)
            instance = form.save()
            return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "%s");</script>' % (instance.pk, instance, id_field))
        return render(request, "add-externo.html", {
            "form": form, 
            'title': 'Agrega una Editorial'
            })

class PalabrasCreatePopup(View):
    def get(self, request, *args, **kwargs):
        form = PalabrasForm()
        return render(request, "add-externo.html", {
            "form": form, 
            'title': 'Agrega una palabra clave'
            })

    def post(self, request, *args, **kwargs):
        form = PalabrasForm(request.POST)
        if form.is_valid():
            id_field = form.cleaned_data.get('id_field')
            print(id_field)
            instance = form.save()
            return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "%s");</script>' % (instance.pk, instance, id_field))
        return render(request, "add-externo.html", {
            "form": form, 
            'title': 'Agrega una palabra clave'
            })

class LineasCreatePopup(View):
    def get(self, request, *args, **kwargs):
        form = LineasForm()
        return render(request, "add-externo.html", {
            "form": form, 
            'title': 'Agrega una Linea de Investigacion'
            })

    def post(self, request, *args, **kwargs):
        form = LineasForm(request.POST)
        if form.is_valid():
            id_field = form.cleaned_data.get('id_field')
            print(id_field)
            instance = form.save()
            return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "%s");</script>' % (instance.pk, instance, id_field))
        return render(request, "add-externo.html", {
            "form": form, 
            'title': 'Agrega una Linea de Investigacion'
            })

class InstitucionCreatePopup(View):
    def get(self, request, *args, **kwargs):
        form = InstitucionForm()
        return render(request, "add-externo.html", {
            "form": form, 
            'title': 'Agrega una Institucion'
            })

    def post(self, request, *args, **kwargs):
        form = InstitucionForm(request.POST)
        if form.is_valid():
            id_field = form.cleaned_data.get('id_field')
            print(id_field)
            instance = form.save()
            return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "%s");</script>' % (instance.pk, instance, id_field))
        return render(request, "add-externo.html", {
            "form": form, 
            'title': 'Agrega una Institucion'
            })

# def paises(request):
#     import csv
#     from django.db import transaction
#     list2 = []
#     with open("/home/urimeba/Downloads/paises.csv", "r", newline="") as f:
#         csv_reader = csv.reader(f, delimiter=",")
#         for row in csv_reader:
#                 print(row[0])
#                 list2.append(row[0])

#     # for p in list2:
#     #     print(p)
#     with transaction.atomic():
#         for pais in list2:
#             Pais.objects.create(nombre=pais)
#     return HttpResponse('Hey')
