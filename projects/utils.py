from django.db.models import Q
from .models import Project, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProjects(request, projects, results):
    # colocamos el numero de pagina a mostrar
    page = request.GET.get('page')
    # cuantos resultados queremos por pagina
    # colocamos el Paginator, que toma el array y cuantos resultados muestra
    paginator =  Paginator(projects, results)
    # hacemos el try para ver si la pagina existe
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        # si no hay pagina, colocamos la pagina 1 como default
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        # si la pagina no existe colocamos la ultima pagina como default
        page = paginator.num_pages
        projects = paginator.page(page)

    # aca colocamos la ventana que se vera la cantidad de paginas en el front
    # colocamos el left y right index para saber hasta donde ira la ventana (cuantos numeros se mostraran)
    left_index = (int(page) - 2)
    if left_index < 1:
        left_index = 1
    right_index = (int(page) + 4)

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
    # colocamos los index en un range y lo enviamos al front
    custom_range = range(left_index, right_index)

    return custom_range, projects


def searchProjects(request):
    # iniciamos con el string vacio para no interferir con nada
    search = ''
    # validamos si el front esta enviando una peticion GET con el name de search
    if request.GET.get('search'):
        # sacamos la data que trae ese GET
        search = request.GET.get('search')
    
    tags = Tag.objects.filter(name__icontains=search)
    # tomamos todos los projectos que estan en la base de datos
    # aca hacemos referencia al modelo y sus conecciones many to many, one to many, etc
    # filtramos por el input de search que viene desde el front
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search) |
        Q(description__icontains=search) |
        # aca lo que sucede es que subimos al parent node, para tomar el nombre y filtrar por el nombre del owner
        Q(owner__name__icontains=search) |
        Q(tags__in=tags)
    )

    return projects, search