from django.conf.urls import url
from corepages.views import home 
from music.views import *

urlpatterns = [
    url('', home),
    url('<slug:title>', track.by_title),
    url('<int:id>', track.by_id)
]
