from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', WorldappHome.as_view(), name='home'),
    path('about/', WorldappAbout.as_view(), name='about'),
    path('addtown/', AddTown.as_view(), name='addtown'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('register/', RegistrUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('country/<slug:code>/', cache_page(20)(WorldappCountry.as_view()), name='country'),
]
