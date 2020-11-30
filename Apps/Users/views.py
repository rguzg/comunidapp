import ast
import json
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponse, redirect, render
from django.views import View
from django.forms.models import model_to_dict
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.db.models import Q
from .forms import (AlumnoForm, ArticuloForm, AuthenticationForm, AutorForm,
                    CapituloLibroForm, CongresoForm, EditorialForm,
                    InstitucionForm, InvestigacionForm, LineasForm,
                    PalabrasForm, PatenteForm, RevistaForm, TesisForm,
                    UserCreationForm, ProfesorCreationForm, UpdateRequestForm, FacultadForm,
                    NivelForm, ContratoForm)
from .models import (Articulo, CapituloLibro, Patente, Congreso, Investigacion, Tesis,  Contrato, Facultad, LineaInvestigacion, Nivel,
                     Pais, User, UpdateRequest, Autor)


"""
Clases para el manejo y administracion de sesiones y de usuarios
"""


class SearchUsers(View):
    def post(self, request, *args, **kwargs):
        # textoBusqueda = request.POST.get('textoBusqueda')
        textoBusqueda = json.load(request)['textoBusqueda'] #Get data from POST request
        print(textoBusqueda)
        # textoBusqueda = 'a'
        users = User.objects.filter(
            Q(username__icontains=textoBusqueda) |
            Q(first_name__icontains=textoBusqueda) |
            Q(last_name__icontains=textoBusqueda) |
            Q(cuerpoAcademico__icontains=textoBusqueda) 
        ).filter(
            is_staff=False,
            is_superuser=False,
            is_active=True
        ).values('id','username', 'foto', 'first_name', 'last_name', 'clave', 'cuerpoAcademico')

        print(users)

        return JsonResponse({'users':list(users)}, safe=False)


class CustomLogin(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    authentication_form = AuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inicia sesión en Comunidapp'
        return context


class Home(ListView):
    template_name = 'home.html'
    paginate_by = 100
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Comunidapp'
        return context

    def get_queryset(self):
        queryset = User.objects.filter(is_superuser=False)
        return queryset


class Perfil(DetailView):
    model = User
    template_name = 'perfil-detail.html'

    def get_context_data(self, **kwargs):
        context = super(Perfil, self).get_context_data(**kwargs)
        user = super().get_object()
        context['title'] = "Perfil de {0}".format(user.get_full_name())
        userId = self.kwargs['pk']

        autor = Autor.objects.get(user_id=userId)
        print(autor)

        articulos = Articulo.objects.filter(Q(primer_autor = autor) | Q(primer_colaborador = autor) | Q(segundo_colaborador = autor) )
        capituloslibros = CapituloLibro.objects.filter(Q(primer_autor = autor) | Q(primer_coautor = autor) | Q(segundo_coautor = autor) )
        patentes = Patente.objects.filter(autores=autor)
        congresos = Congreso.objects.filter(Q(primer_autor = autor) | Q(primer_colaborador = autor) | Q(segundo_colaborador = autor) )
        investigaciones = Investigacion.objects.filter(Q(primer_colaborador = autor) | Q(segundo_colaborador = autor) )
        tesis = Tesis.objects.filter(profesor=self.request.user)

        context['articulos'] = articulos
        context['capituloslibros'] = capituloslibros
        context['patentes'] = patentes
        context['congresos'] = congresos
        context['investigaciones'] = investigaciones
        context['tesis'] = tesis

        return context


class Profile(SuccessMessageMixin, FormView):
    form_class = UpdateRequestForm
    template_name = 'my_profile.html'
    success_url = '/profile'
    success_message = 'Petición de actualización enviada correctamente'

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)

        is_peticion = UpdateRequest.objects.filter(
            user=self.request.user, estado='P').count()
        if is_peticion > 0:
            context['is_peticion'] = True
        else:
            peticion = UpdateRequest.objects.get(user=self.request.user)
            if peticion.estado == 'R':
                context['peticion'] = peticion

        context['title'] = "Actualización de mis datos"
        context['producto'] = 'actualizacion'

        return context

    def get_initial(self):
        """
        Regresando la informacion del usuario al formulario,
        ya que no es un ModelForm
        """
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['email'] = self.request.user.email
        initial['clave'] = self.request.user.clave
        initial['sexo'] = self.request.user.sexo
        if self.request.user.nacimiento:
            initial['nacimiento'] = self.request.user.nacimiento.strftime("%d-%m-%Y")
        initial['foto'] = self.request.user.foto
        initial['grado'] = self.request.user.grado
        initial['contratacion'] = self.request.user.contratacion
        initial['cuerpoAcademico'] = self.request.user.cuerpoAcademico
        initial['publico'] = self.request.user.publico
        initial['user'] = self.request.user
        initial['niveles'] = [
            nivel for nivel in self.request.user.niveles.all().values_list('id', flat=True)]
        initial['facultades'] = [
            facultad for facultad in self.request.user.facultades.all().values_list('id', flat=True)]
        initial['investigaciones'] = [
            investigacion for investigacion in self.request.user.investigaciones.all().values_list('id', flat=True)]
        return initial

    def post(self, request, *args, **kwargs):
        peticion = UpdateRequest.objects.filter(user=request.user).first()

        if peticion:
            print('Si existe una instancia')
            form = UpdateRequestForm(
                request.POST, request.FILES, instance=peticion)
        else:
            print('No existe una instancia ')
            form = UpdateRequestForm(request.POST, request.FILES)

        if form.is_valid():
            print('Formulario valido')
            peticion_obj = form.save(commit=False)
            peticion_obj.user = request.user
            peticion_obj.estado = 'P'
            peticion_obj.changed_fields = {'fields': form.changed_data}

            print(form)
            if 'foto' in form:
                print('SI HAY FOTO')

            peticion_obj.save()

            form.save_m2m()

        messages.add_message(self.request, messages.SUCCESS,
                             'Petición de actualización enviada correctamente')
        return render(request, self.template_name, {
            'form': form,
            'title': "Actualización de mis datos",
            'producto': 'actualizacion'
        })

    def form_valid(self, form):
        """
        Funcion que detecta que campos cambiaron y guarda unicamente los cambiados
        """
        cleaned_data = form.cleaned_data
        changed_data = form.has_changed
        print('--------------------------------------------------------------')

        peticion, created = UpdateRequest.objects.get_or_create(
            user=self.request.user)
        peticion.estado = 'P'
        peticion.__dict__.update(changed_data)
        peticion.save()
        return super().form_valid(form)


class CustomLogout(LogoutView):
    next_page = 'login'


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


class UpdatedUsers(ListView):
    model = UpdateRequest
    paginate_by = 10
    template_name = 'updates.html'
    ordering = ['-created']

    def get_queryset(self):
        return UpdateRequest.objects.filter(estado='P')

    def post(self, request, *args, **kwargs):
        idPeticion = request.POST['id']
        comentario = request.POST['comentario-'+idPeticion]
        rechazado = request.POST.get('Rechazado')
        query = UpdateRequest.objects.get(id=idPeticion)

        if rechazado:
            query.estado = 'R'
            query.motivo = comentario
            query.save()
            return redirect('/updates')
        else:
            query.estado = 'A'
            query.motivo = None
            query.save()

        query = UpdateRequest.objects.get(id=idPeticion)
        niveles_peticion = query.niveles.all()
        facultades_peticion = query.facultades.all()
        investigaciones_peticion = query.investigaciones.all()

        user = User.objects.filter(id=query.user.id)
        something = model_to_dict(query)

        del something['id']
        del something['user']
        del something['estado']
        del something['motivo']
        del something['changed_fields']
        del something['facultades']
        del something['investigaciones']
        del something['niveles']

        user.update(**something)

        user[0].niveles.set(niveles_peticion)
        user[0].facultades.set(facultades_peticion)
        user[0].investigaciones.set(investigaciones_peticion)

        return redirect('updates')

    def get_context_data(self, **kwargs):
        context = super(UpdatedUsers, self).get_context_data(**kwargs)
        context['title'] = 'Peticiones de actualización'
        return context


"""
CBV para la creacion de usuarios administradores y profesores
"""


class AddAdminUsers(SuccessMessageMixin, CreateView):
    template_name = 'users.html'
    form_class = UserCreationForm
    success_url = '/add/admin'
    success_message = 'Administrador creado correctamente'

    def get_initial(self):
        initial = super(AddAdminUsers, self).get_initial()
        initial = initial.copy()
        initial['is_superuser'] = True
        initial['is_staff'] = True
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super(AddAdminUsers, self).get_context_data(*args, **kwargs)
        context['title'] = 'Agrega un usuario Administrador'
        context['producto'] = 'administrador'
        return context


class AddProfesorUsers(SuccessMessageMixin, CreateView):
    template_name = 'users.html'
    form_class = ProfesorCreationForm
    success_url = '/add/profesor'
    success_message = 'Profesor creado correctamente'

    # Necesario poner el username y el email iguales

    def get_initial(self):
        initial = super(AddProfesorUsers, self).get_initial()
        initial = initial.copy()
        initial['publico'] = True
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Agrega un usuario Profesor'
        context['producto'] = 'profesor'
        return context

    # Necesario para guardar los campos M2M
    def form_valid(self, form):
        form_valid = super(AddProfesorUsers, self).form_valid(form)
        form_val = form.save(commit=False)
        form_val.save()
        form.save_m2m()
        return form_valid


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
        context['producto'] = 'articulo'
        return context


class AddCapituloLibro(SuccessMessageMixin, CreateView):
    template_name = 'add-producto.html'
    form_class = CapituloLibroForm
    success_url = '/new/libro'
    success_message = 'Libro/Capítulo creado correctamente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agrega un libro o capítulo'
        context['producto'] = 'libro'
        return context


class AddPatente(SuccessMessageMixin, CreateView):
    template_name = 'add-producto.html'
    form_class = PatenteForm
    success_url = '/new/patente'
    success_message = 'Patente creada correctamente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agrega una patente'
        context['producto'] = 'patente'
        return context


class AddCongreso(SuccessMessageMixin, CreateView):
    template_name = 'add-producto.html'
    form_class = CongresoForm
    success_url = '/new/congreso'
    success_message = 'Participacion en congreso creada correctamente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agrega un partición en congreso'
        context['producto'] = 'congreso'
        return context


class AddInvestigacion(SuccessMessageMixin, CreateView):
    template_name = 'add-producto.html'
    form_class = InvestigacionForm
    success_url = '/new/investigacion'
    success_message = 'Proyecto de Investigacion/Vinculacion agregado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agrega un proyecto de investigación'
        context['producto'] = 'investigacion'
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
        context = super(AddTesis, self).get_context_data(*args, **kwargs)
        context['title'] = 'Agrega una dirección de tesis'
        context['producto'] = 'tesis'
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
            instance = form.save()
            return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "%s");</script>' % (instance.pk, instance, id_field))
        return render(request, "add-externo.html", {
            "form": form,
            'title': 'Agrega una Institucion'
        })


class FacultadCreatePopup(View):
    def get(self, request, *args, **kwargs):
        form = FacultadForm()
        return render(request, "add-externo.html", {
            "form": form,
            'title': 'Agrega una Facultad'
        })

    def post(self, request, *args, **kwargs):
        form = FacultadForm(request.POST)
        if form.is_valid():
            id_field = form.cleaned_data.get('id_field')
            instance = form.save()
            return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "%s");</script>' % (instance.pk, instance, id_field))
        return render(request, "add-externo.html", {
            "form": form,
            'title': 'Agrega una Facultad'
        })


class NivelesCreatePopup(View):
    def get(self, request, *args, **kwargs):
        form = NivelForm()
        return render(request, "add-externo.html", {
            "form": form,
            'title': 'Agrega un Nivel'
        })

    def post(self, request, *args, **kwargs):
        form = NivelForm(request.POST)
        if form.is_valid():
            id_field = form.cleaned_data.get('id_field')
            instance = form.save()
            return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "%s");</script>' % (instance.pk, instance, id_field))
        return render(request, "add-externo.html", {
            "form": form,
            'title': 'Agrega un Nivel'
        })


class ContratoCreatePopup(View):
    def get(self, request, *args, **kwargs):
        form = ContratoForm()
        return render(request, "add-externo.html", {
            "form": form,
            'title': 'Agrega un tipo de Contrato'
        })

    def post(self, request, *args, **kwargs):
        form = ContratoForm(request.POST)
        if form.is_valid():
            id_field = form.cleaned_data.get('id_field')
            instance = form.save()
            return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "%s");</script>' % (instance.pk, instance, id_field))
        return render(request, "add-externo.html", {
            "form": form,
            'title': 'Agrega un tipo de Contrato'
        })