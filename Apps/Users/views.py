from django.shortcuts import render, redirect, HttpResponse
import json
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import PasswordChangeForm
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView, FormView, CreateView
from .models import User, UserActualizado, Nivel, Facultad, LineaInvestigacion, Contrato, Pais, Articulo
from .forms import UserActualizadoForm, AuthenticationForm, ArticuloForm, CapituloLibroForm, PatenteForm, CongresoForm, InvestigacionForm, TesisForm, AutorForm, RevistaForm, EditorialForm, PalabrasForm
import ast
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# CBV para el Login (necesario LOGIN_URL, LOGIN_REDIRECT_URL y LOGOUT_REDIRECT_URL en SETTINGS)
class CustomLogin(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    authentication_form = AuthenticationForm

# CBV para el HTML de Home
class Home(ListView):
    template_name = 'home.html'
    paginate_by = 20
    model = User

    # def get_queryset(self):
    #     queryset = User.objects.filter(is_superuser=False)
    #     return queryset

# CBV para el HTML del detalle de cada usuario
class Perfil(DetailView):
    model = User
    template_name = 'perfil-detail.html'

# CBV para el HTML donde se muestra el perfil del usuario
class Profile(FormView):
    form_class = UserActualizadoForm
    template_name = 'my_profile.html'
    success_url = '/'

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
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Contraseña cambiada correctamente')

        return render(request, 'password.html', {
            'form': form
        })

# CBV para aprobar o rechazar peticion de cambio de perfil
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
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        # import ast
        # print(ast.literal_eval("{'email': 'email@gmail.com2', 'clave': 2, 'sexo': 'H'}"))
        return context

class AddArticulo(SuccessMessageMixin, CreateView):
    template_name = 'add-articulo.html'
    form_class = ArticuloForm
    success_url = '/new/article'
    success_message = 'Articulo creado correctamente'

class AddCapituloLibro(SuccessMessageMixin, CreateView):
    template_name = 'add-capituloLibro.html'
    form_class = CapituloLibroForm
    success_url = '/new/bookChapter'
    success_message = 'Libro/Capitulo creado correctamente'


# class AddProduct(TemplateView):
    # template_name = "add-product.html"

    # def get_context_data(self, **kwargs):
    #     context = super(AddProduct, self).get_context_data(**kwargs)
    #     context['ArticuloForm'] = ArticuloForm(prefix='ArticuloForm')
    #     context['CapituloLibroForm'] = CapituloLibroForm(prefix='CapituloLibro')
    #     context['PatenteForm'] = PatenteForm(prefix='PatenteForm')
    #     context['CongresoForm'] = CongresoForm(prefix='CongresoForm')
    #     context['InvestigacionForm'] = InvestigacionForm(prefix='InvestigacionForm')
    #     context['TesisForm'] = TesisForm(prefix='TesisForm')
    #     context['title'] = 'Agrega un producto'

    #     # post = self.request.POST.copy()
    #     invalid_articulo = self.request.session['invalid_articulo']
    #     print('Si esta entrando')
    #     if(invalid_articulo):
    #         print('Formulario incorrecto')
    #         context['ArticuloForm'] = ArticuloForm(invalid_articulo, prefix='ArticuloForm')
    #     return context

# class AddArticulo(View):
#     def post(self, request, *args, **kwargs):
#         form = ArticuloForm(request.POST, prefix='ArticuloForm')
#         # print(form)
#         if form.is_valid():
#             instance = form.save()
#             # return render('add-product')
#         else:
#             print(form.errors)
#             request.session['invalid_articulo'] = form
#             print(request.session['invalid_articulo'])
#         # return render(request, "add-product.html", {"form": form})
#         return redirect('add-product')
        

    

class AutorCreatePopup(View):
    def get(self, request, *args, **kwargs):
        form = AutorForm()
        return render(request, "form_autor.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = AutorForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "id_ArticuloForm-primer_autor");</script>' % (instance.pk, instance))
        return render(request, "form_autor.html", {"form": form})

class RevistaCreatePopup(View):
    def get(self, request, *args, **kwargs):
        form = RevistaForm()
        return render(request, "form_revista.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = RevistaForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "id_ArticuloForm-revista");</script>' % (instance.pk, instance))
        return render(request, "form_revista.html", {"form": form})

class EditorialCreatePopup(View):
    def get(self, request, *args, **kwargs):
        form = EditorialForm()
        return render(request, "form_editorial.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = EditorialForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "id_ArticuloForm-editorial");</script>' % (instance.pk, instance))
        return render(request, "form_editorial.html", {"form": form})

class PalabrasCreatePopup(View):
    def get(self, request, *args, **kwargs):
        form = PalabrasForm()
        return render(request, "form_palabras.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = PalabrasForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "id_ArticuloForm-palabras_clave");</script>' % (instance.pk, instance))
        return render(request, "form_palabras.html", {"form": form})

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

