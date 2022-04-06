from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', WorldappHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', addpage, name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('country/<slug:code>/', WorldappCountry.as_view(), name='country'),
]
