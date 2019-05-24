from django.urls import path
from corepages.views import *

urlpatterns = [
    path('home', home, name='home'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('about', about, name='about'),
    path('graphism', graphism, name='graphism'),
    path('search', search, name='search'),
    path('legal', legal, name='legal'),
    path('stats', stats, name='stats'),
    path('videos', videos, name='videos'),
    path('', home, name='home'),
]