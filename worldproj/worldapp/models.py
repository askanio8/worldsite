from django.db import models

# Create your models here.
from django.urls import reverse


class City(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=35)
    countrycode = models.ForeignKey('Country', models.DO_NOTHING, db_column='CountryCode')
    district = models.CharField(db_column='District', max_length=20)
    population = models.IntegerField(db_column='Population')  # verbose_name='Население'

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'city'
        verbose_name = 'Города'
        verbose_name_plural = 'Города'
        ordering = ['-population']


class Country(models.Model):
    code = models.CharField(db_column='Code', primary_key=True, max_length=3, verbose_name='Код')
    name = models.CharField(db_column='Name', max_length=52, verbose_name='Название')
    continent = models.CharField(db_column='Continent', max_length=13, verbose_name='Континент')
    region = models.CharField(db_column='Region', max_length=26, verbose_name='Регион')
    surfacearea = models.FloatField(db_column='SurfaceArea', verbose_name='Площадь')
    indepyear = models.SmallIntegerField(db_column='IndepYear', blank=True, null=True, verbose_name='Год независимости')
    population = models.IntegerField(db_column='Population', verbose_name='Население')
    lifeexpectancy = models.FloatField(db_column='LifeExpectancy', blank=True, null=True, verbose_name='Продолжитенльность жизни')
    gnp = models.FloatField(db_column='GNP', blank=True, null=True)
    gnpold = models.FloatField(db_column='GNPOld', blank=True, null=True)  # Field name made lowercase.
    localname = models.CharField(db_column='LocalName', max_length=45, verbose_name='Самоназвание')
    governmentform = models.CharField(db_column='GovernmentForm', max_length=45, verbose_name='Тип управления')
    headofstate = models.CharField(db_column='HeadOfState', max_length=60, blank=True, null=True)
    capital = models.IntegerField(db_column='Capital', blank=True, null=True, verbose_name='Столица')
    code2 = models.CharField(db_column='Code2', max_length=2)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('country', kwargs={'code': self.code})

    class Meta:
        managed = False
        db_table = 'country'
        verbose_name = 'Страны'
        verbose_name_plural = 'Страны'
        ordering = ['name']