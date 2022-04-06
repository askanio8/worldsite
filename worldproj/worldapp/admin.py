from django.contrib import admin
from .models import *
# Register your models here.

class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'population')
    #list_display_links = ('id', 'name', 'population')
    search_fields = ('id', 'name', 'population')
    list_editable = ('name', 'population')
    #list_filter = ('name', 'population')

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'population')
    search_fields = ('id', 'name', 'population')


admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)