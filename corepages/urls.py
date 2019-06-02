from django.urls import path
from corepages.views import *

urlpatterns = [
    path('home/', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('graphism/', graphism, name='graphism'),
    path('search/', search, name='search'),
    path('legal/', legal, name='legal'),
    # TODO: make /stats/ redirect to /statistics/
    path('stats/', stats, name='stats'),
    path('statistics/', stats, name='stats'),
    path('videos/', videos, name='videos'),
    path('brand-resources/', brand_resources, name='brand_resources'),
    path('', home, name='home'),
]