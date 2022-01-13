# aca crearemos todas las funciones que nos ayuden en la app,
# asi creamos un codigo mas limpio ya que no colocaremos tantas funciones en el archivo views
from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProfiles(request, profiles, results):
    # colocamos el numero de pagina a mostrar
    page = request.GET.get('page')
    # cuantos resultados queremos por pagina
    # colocamos el Paginator, que toma el array y cuantos resultados muestra
    paginator =  Paginator(profiles, results)
    # hacemos el try para ver si la pagina existe
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        # si no hay pagina, colocamos la pagina 1 como default
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        # si la pagina no existe colocamos la ultima pagina como default
        page = paginator.num_pages
        profiles = paginator.page(page)

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

    return custom_range, profiles


def searchProfiles(request):
    # iniciamos con el string vacio para no interferir con nada
    search = ''
    # validamos si el front esta enviando una peticion GET con el name de search
    if request.GET.get('search'):
        # sacamos la data que trae ese GET
        search = request.GET.get('search')
    # nos traemos las skills
    skills = Skill.objects.filter(name__icontains=search)
    # con filter usando icontains podemos filtrar siendo case insensitive,
    # asi solo aparecen los usuarios con el filtro que el usuario pase
    # usando Q colocamos | para hacer que este en el nombre OR en la short description
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search) | 
        Q(short_intro__icontains=search) | 
        Q(skill__in=skills)
        )

    return profiles, search