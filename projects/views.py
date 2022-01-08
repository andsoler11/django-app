from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required

# el objeto request trae la informacion que llega desde el front
def projects(request):
    # tomamos todos los projectos que estan en la base de datos
    # aca hacemos referencia al modelo y sus conecciones many to many, one to many, etc
    projects = Project.objects.all()
    # pasamos los proyectos al dict context para pasrlos al front
    context = {'projects': projects}
    # retornamos con el render de la vista html y su data del dict context
    return render(request, 'projects/projects.html', context)

# aca usamos pk como primary key, que es enviada desde el front
# asi podemos filtrar desde el id = pk
def project(request, pk):
    # filtramos para solo mostrar 1 proyecto y su informacion
    projectObj = Project.objects.get(id=pk)
    # devolvemos el render de la vista html, junto con la informacion del proyecto 
    return render(request, 'projects/single-project.html', {'project': projectObj})


# con este decorador hacemos que el usuario tiene que estar contectado para poder ver la vista
@login_required(login_url='login')
def createProject(request):
    # sacamos el usuario que esta conectado del objeto request
    profile = request.user.profile
    # traemos el formulario del projecto que tenemos en nuestro forms.py
    form = ProjectForm()
    # si la peticion es POST entonces entra aca
    if request.method == 'POST':
        # usamos el request.files por que estamos enviando un archivo(foto)
        # colocamos ambas en una variable para luego guardar en la base de datos
        form = ProjectForm(request.POST, request.FILES)
        # checkeamos que la data sea correcta
        if form.is_valid():
            # todavia no guardamos en la base de datos, por que tenemos que guardar la informacion
            # solo para el usuario que creo el porjecto, por eso usamos commit=false
            # asi guardamos la informacion que viene del formulario en una variable pero no en la BD
            project = form.save(commit=False)
            # aca asignamos el owner del projecto creado, lo colocamos como el profile que sacamos del request
            project.owner = profile
            # guardamos la data en la base de datos y redireccionamos a la vista account
            project.save()
            return redirect('account')

    # sacamos el contexto para mostrar el formulario del proyecto que estamos editando
    context = {'form': form}
    # renderizxamos la vista html
    return render(request, "projects/project_form.html", context)


# tiene que estar logeado para ver esta vista
@login_required(login_url='login')
def updateProject(request, pk):
    #sacamos el usuario del objeto request ya que tiene que estar logeado para ver esta vista
    profile = request.user.profile
    # aca tomamos la data del proyecto que el usuario va a editar, la data esta en la BD entonces
    # usamos una relacion usando project.set(get) y le pasamos el id del proyecto a editar (pk)
    project = profile.project_set.get(id=pk)
    # hacemos una instancia del formulario, con la informacion del proyecto que el usuario va a editar
    # por eso colocamos instance=project
    form = ProjectForm(instance=project)
    # validamos que el metodo sea POST, si no pues renderizamos la vista
    if request.method == 'POST':
        # colocamos la data que el usuario actualizo, files por que pueden ser archivos(foto)
        form = ProjectForm(request.POST, request.FILES, instance=project)
        # verificamos que la data sea valida
        if form.is_valid():
            # guardamos en la BD y redireccionamos
            form.save()
            return redirect('account')

    # colocamos el contexto del formulario que el usuario va a ver
    context = {'form': form}
    # renderizamos la vista
    return render(request, "projects/project_form.html", context)


# requiere login
@login_required(login_url='login')
def deleteProject(request, pk):
    # sacamos el profile, para borrar solo el projecto del usuario logeado
    profile = request.user.profile
    # usamos el project_set.get() para traernos el projecto que este asociado a ese usuario
    project =  profile.project_set.get(id=pk)
    # validamos el metodo POST si no pues renderizamos vista
    if request.method == 'POST':
        # borramos de la BS y redireccionamos
        project.delete()
        return redirect('projects')
    
    # colocamos el projecto como el objeto a eliminar si se da confirmar en la vista de delete html
    context = {'object': project}
    # renderizamos la vista de delete template
    return render(request, "delete_template.html", context)
