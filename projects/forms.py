from django.forms import ModelForm, fields
from django import forms
from .models import Project

# aca colocamos las clases para nuestros formularios
# esto nos facilita la creacion de formularios en el front
# ya que traemos la data de nuestros modelos, y mostramos los compos requeridos que necesita el modelo
class ProjectForm(ModelForm):
    # colocamos la clase meta para poder especicar los campos que queremos y los que no
    class Meta:
        # colocamos el modelo Porject de nuestros modelos.py
        model = Project
        # espeficiamos los campos que queremos que se muestren
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']
        # colocamos que los tags, van a ser un checkbbox multiple
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
    # aca los que vamos a hacer es modificar los atributos de los campos del modelo que mostraremos
    def __init__(self, *args, **kwargs):
        # heredamos de la clase padre
        super(ProjectForm, self).__init__(*args, **kwargs)
        # y aca vamos a cambiar el atributo clase para usarlo como class=input
        # asi el css se renderiza mejor
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        # self.fields['title'].widget.attrs.update({ 
        #     'class':'input', 
        #     'placeholder': 'Add Title' 
        # })

        # self.fields['description'].widget.attrs.update({ 
        #     'class':'input',  
        # })