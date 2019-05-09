from django.conf.urls import url
from corepages.views import *

urlpatterns = [
    url('home', home),
    url('music', music),
    url('about', about),
    url('contact', contact),
    url('about', about),
    url('graphism', graphism),
    url('search', search),
    url(r'^$', home),
]