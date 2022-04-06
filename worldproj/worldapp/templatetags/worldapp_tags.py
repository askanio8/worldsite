from django import template
from django.db.models import Count

from worldapp.models import *


register = template.Library()

@register.simple_tag()
def get_countries():
    return Country.objects.all()

@register.simple_tag()
def get_continents():
    query = Country.objects.values('continent').distinct()  # distinct тут не работет?
    continents = [c['continent'] for c in query]
    return set(continents)
