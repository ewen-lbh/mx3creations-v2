from django.conf.urls import url
from music.views import *

urlpatterns = [
    url(r'^$', music, name='music'),
    url('<slug:title>', track.by_title, name='track'),
    url('<int:id>', track.by_id, name='track')
]
