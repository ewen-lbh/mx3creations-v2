from django.conf.urls import url
from corepages.views import *

urlpatterns = [
    url('home', home, name='home'),
    url('about', about, name='about'),
    url('contact', contact, name='contact'),
    url('about', about, name='about'),
    url('graphism', graphism, name='graphism'),
    url('search', search, name='search'),
    url('legal', legal, name='legal'),
    url('stats', stats, name='stats'),
    url(r'^$', home, name='home'),
]