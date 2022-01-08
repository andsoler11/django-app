from django.contrib import admin

# Register your models here.
from .models import Project, Review, Tag

# aca registramos los modelos para poderlos ver en la vista del admin
admin.site.register(Project)
admin.site.register(Review)
admin.site.register(Tag)

