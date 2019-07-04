from django.urls import path
from corepages.views import *

urlpatterns = [
    path('home/', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('search/', search, name='search'),
    path('search/<q>', search, name='search'),
    path('legal/', legal, name='legal'),
    path('stats/', lambda req: HttpResponseRedirect('/statistics/'), name='stats'),
    path('statistics/', stats, name='stats'),
    path('brand-resources/', brand_resources, name='brand_resources'),
    path('', home, name='home'),
]