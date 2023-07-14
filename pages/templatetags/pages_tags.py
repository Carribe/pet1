from django import template
from pages.models import *

register = template.Library()

@register.simple_tag()
def get_film_type():
    return FilmType.objects.all()