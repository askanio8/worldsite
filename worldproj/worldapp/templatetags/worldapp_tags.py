from django import template
from django.db.models import Count

from worldapp.models import *


register = template.Library()

@register.simple_tag()
def get_countries_by_continets():
    continents = {}
    continents['Asia'] = Country.objects.filter(continent='Asia')
    continents['Africa'] = Country.objects.filter(continent='Africa')
    continents['Europe'] = Country.objects.filter(continent='Europe')
    continents['Oceania'] = Country.objects.filter(continent='Oceania')
    continents['North America'] = Country.objects.filter(continent='North America')
    continents['South America'] = Country.objects.filter(continent='South America')
    return continents
