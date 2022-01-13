from django.db import models
from django.db.models.base import Model
import uuid
from users.models import Profile
# Create your models here.




# comenzamos con los modelos de los proyectos, esto por asi decirlo colocara las columnas en la base de datos
# entonces es como una tabla Project con sus respectivas columnas que especificamos en la clase
class Project(models.Model):
    # comenzamos con owner, para saber a quien le pertenece este proyecto
    # se usa foreignKey para decirle que el owner esta asociado con el profile en la tabla profile de la BD
    # el on_delete es para saber que pasa si borramos el proyecto, SET_NULL es que no va a borrar el profile, pero dejara null en el proyecto borrado
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    # colocamos el titulo 
    title = models.CharField(max_length=255)
    # descripcion
    description = models.TextField(null=True, blank=True)
    # la imagen, aca colocamos default y el nombre de la imagen que queremos como default
    # esta imagen esta en el archivo de staticFiles, el cual tenemos que trazar la ruta desde el 
    # settings en nuestro archivo principal(devsearch)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    # aca colocamos un Many to Many ya que muchos proyectos pueden tener muchos tags distintos, colocamos el nombre Tag para 
    # hacer referencia a la clase que esta asociado (la clase esta mas abajo de este archivo)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    # esto es para que automaticamente se nos creen las fechas al momento de crear el proyecto
    created = models.DateTimeField(auto_now_add=True)
    # colocamos el id del  proyecto, esto usando uuid que importamos, y colocamos como primary Key
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    # aca es para que cuando imprimamos el proyecto, salga el titulo del proyecto
    def __str__(self):
        return self.title

    # class meta para modificar los ajustes por defecto
    class Meta:
        # cambiar el orden en que se muestran los proyectos
        # se coloca el "-" para colocarlo en forma Desc sin el - seria Asc
        ordering = ['-created']

# hacemos el modelo de review
class Review(models.Model):
    # creamos la tupla con los tipos de votos que colocaremos
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )

    # owner = 
    # colocamos el foreign Key ya que las reviews estaran asociadas el proyecto que le daremos el review
    # en ondelete cascade significa que si se borra el proyecto, las reviews tambien se borraran
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    # colcoamos el value con los tipos de votos que pueden hacer, especificado en la tupla que creamos
    value = models.CharField(max_length=255, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    # aca para cuando imprimamos pues salgan cuantos votos tiene el proyecto
    def __str__(self):
        return self.value

# creamos la clase para los tags que tendra el proyecto
class Tag(models.Model):
    # nombre del tag
    name = models.CharField(max_length=255)
    # fecha autmaticamente creada, de cuando se creo el tag
    created = models.DateTimeField(auto_now_add=True)
    # id usando uuid
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    # modificamos cuando imprimimos, asi sale es el nombre del tag
    def __str__(self):
        return self.name

