# aca crearemos todas las funciones que nos ayuden en la app,
# asi creamos un codigo mas limpio ya que no colocaremos tantas funciones en el archivo views
from .models import Profile, Skill
from django.db.models import Q

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