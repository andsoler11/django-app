from django.db.models import Q
from .models import Project, Tag

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