from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q

from projects.views import projects
from .models import Profile, Skill
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .utils import searchProfiles, paginateProfiles
# Create your views here.

# empezamos con la vista del usuario al logearse
def loginUser(request):
    # colocamos el nombre de la pagina
    page = 'login'
    context = {'page': page}
    # si el usuario ya esta logeado pues redireccionamos a  la pagina profiles
    if request.user.is_authenticated:
        return redirect('profiles')

    # si el request nos trae una peticion POSt esto es por que el usuario se esta logeando
    if request.method == 'POST':
        # colocamos los campos en variables
        username = request.POST['username'].lower()
        password = request.POST['password']
        # traemos el usuario de la BD (esto usando el modelo User creado en models.py)
        try:
            user = User.objects.get(username = username)
        except:
            # esto por si el usuario no existe entonces que arroje el error
            messages.error(request, 'Username doest not exist')
        # vamos a autentificar si el usuario y contrasenia son correctas
        user = authenticate(request, username=username, password=password)
        # si el usuario y contrasenia es correcto entonces logeamos al usuario y redireccionamos
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            # si estan mal, entonces mostramos error
            messages.error(request, 'username or password is incorrect')
    # si no hay peticiones post y el usuario no esta logeado entonces mostramos la vista html
    return render(request, 'users/login_register.html', context)



# logout del usuario
def logoutUser(request):
    # simplemente hacemos logout del request, que trae el usuario logeado y redireccionamos
    logout(request)
    messages.info(request, 'User was logout')
    return redirect('login')


# registro del usuario
def registerUser(request):
    # colocamos el nombre de la pagina
    page = 'register'
    # traemos el formulario de la clase de formularios que creamos en forms.py
    form = CustomUserCreationForm
    # si la peticion es POST entonces es por que el usuario se esta registrando
    if request.method == 'POST':
        # sacamos la data del formulario
        form = CustomUserCreationForm(request.POST)
        # validamos is la data es correcta
        if form.is_valid():
            # sacamos la informacion del formulario, sin guardar en la BD, asi podemos asignar un username al profile que acaban de crear
            user = form.save(commit=False)
            # colocamos el username
            user.username = user.username.lower()
            #guardamos ahora si en la BD
            user.save()
            # sacamos el mensaje, logeamos al usuario y redireccionamos
            messages.success(request, 'User account was created!')
            login(request, user)
            return redirect('edit-account')

        else:
            # sacamos mensaje de error si algo falla
            messages.error(request, 'An error has occurred during registration')
    
    # si no hay peticiones ni nada, entonces renderzamos la vista
    # colcoamos el nombre de la pagina y su formulario que traemos de la clase form.py
    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)



# funcione para buscar perfiles!
def profiles(request):
    # llamamos a la funcion de search que creamos en el archivo utils.py
    profiles, search = searchProfiles(request)

    # llamamos a la funcion de paginacion
    custom_range, profiles = paginateProfiles(request, profiles, 6)

    # pasamos el contexto, con los perfiles que trae el filtro, 
    # y con el valor del search para que este en el formulario,
    # asi el usuario sabe que fue lo que busco
    context = {'profiles': profiles, 'search': search, 'custom_range': custom_range}

    return render(request, 'users/profiles.html', context)





def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")


    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile, 'skills': skills, 'projects': projects}

    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'skill was added successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'skill was added updated!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'skill was deleted successfully!')
        return redirect('account')

    context = {'object': skill}
    return render(request, 'delete_template.html', context)