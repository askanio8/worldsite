import logging
import os
import sys

from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Avg, Count
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView, TemplateView, UpdateView

from .forms import AddPostForm, RegisterUserForm, LoginUserForm, ContactForm, UpdatePostForm, FilterForm
from .models import *
from .utils import *

logger = logging.getLogger(__name__)

class WorldappHome(DataMixin, ListView):
    model = City
    template_name = 'worldapp/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Main')
        context['count'] = len(context['posts'])
        if len(context['posts']) > 0:
            context['sumpopulation'] = round(sum([c.population for c in context['posts']])/ len(context['posts']))
        context['form'] = FilterForm()
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        part_name = self.request.GET.get('part_name', default='')
        min_population = self.request.GET.get('min_population', default='')
        max_population = self.request.GET.get('max_population', default='')
        min_population = min_population if min_population.isdigit() else 0
        max_population = max_population if max_population.isdigit() else 1000000000
        return City.objects.filter(name__contains=part_name, population__gte=min_population,
                                   population__lte=max_population).select_related('countrycode')


class WorldappCountry(DataMixin, ListView):
    model = City
    template_name = 'worldapp/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = len(context['posts'])
        context['sumpopulation'] = round(sum([c.population for c in context['posts']])/ len(context['posts']))
        c_def = self.get_user_context(title = context['posts'][0].countrycode)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return City.objects.filter(countrycode=self.kwargs['code']).select_related('countrycode')


class AddTown(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'worldapp/addtown.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')  # без этого будет 404
    #raise_exception = True  # с этим 403. если не класс а ф-я, то исп декоратор

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Add Town')
        return dict(list(context.items()) + list(c_def.items()))


class UpdateTown(LoginRequiredMixin, DataMixin, UpdateView):
    form_class = UpdatePostForm
    template_name = 'worldapp/updatetown.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')  # без этого будет 404
    #raise_exception = True  # с этим 403. если не класс а ф-я, то исп декоратор

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Update Town')
        context['pk'] = self.kwargs['pk']
        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, queryset=None):
        return City.objects.get(pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        town = City.objects.get(pk=self.kwargs['pk'])
        town.name = request.POST.get('name')
        town.countrycode = Country.objects.get(code=request.POST.get('countrycode'))
        town.district = request.POST.get('district')
        town.population = request.POST.get('population')
        town.save()

        # логирование
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = None
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        logger.warning(f'updated city {town} from ip: {ip} by user {request.user.username}')

        return redirect('home')


class RegistrUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'worldapp/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Register')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):  # при успешной регистрации, логиним автоматически
        user = form.save()  # сохраняем форму в бд вручную
        login(self.request, user)  # стандартная ф-я django
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm  #AuthenticationForm стандартная
    template_name = 'worldapp/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Login")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')

class WorldappAbout(DataMixin, TemplateView):
    template_name = 'worldapp/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'About')
        return dict(list(context.items()) + list(c_def.items()))


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'worldapp/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Feedback")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        #print(form.cleaned_data)  # здесь нужно сделать отправку email

        # нужен еще пароль логин в settings.py
        #from django.core.mail import EmailMessage
        #email = EmailMessage('Subject', 'Body', to=['askanio8@gmail.com'])
        #email.send()
        return redirect('home')


# для сравнения ф-я обработчик
def index(request):
    posts = Country.objects.all()
    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Главная страница'
    }

    return render(request, 'worldapp/index.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
