from django.urls import path
# importamos las vistas
from . import views

# aca colcoamos las rutas, lo que el usuario vera si consulta una ruta espeficicada,
# renderizamos la vista especifica de cada tura, el name= nos sirve para usarlo mas facil en
# el front (html) y el <str:pk> es para pasar el id de un proyecto
# este archivo lo creamos en cada aplicacion espefica asi no saturamos las rutas en nuestro
# archivo principal (devsearch)
urlpatterns = [
    # colocamos la vista principal, esta aparece, si el usuario da click en projects/
    # lo colocamos como '' en vez de proyects ya que en el archivo de las rutas principales (devsearch)
    # especificamos que las rutas de aca siemrpe empezaran con projects/
    # entonces todas las rutas aca traen por defecto projects/
    # ej projects/project/1919191
    # tambien usamos view. para renderizar la vista especificada en la funcion en el arhivo de views.py
    path('', views.projects, name="projects"),
    path('project/<str:pk>/', views.project, name="project"),
    path('create-project/', views.createProject, name="create-project"),
    path('update-project/<str:pk>/', views.updateProject, name="update-project"),
    path('delete-project/<str:pk>/', views.deleteProject, name="delete-project"),
]
