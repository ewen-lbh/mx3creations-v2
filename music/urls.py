from django.conf.urls import url
from music.views import *

urlpatterns = [
    url('music', music, name='music'),
    url('listen/<slug:title>', track.by_title, name='track'),
    url('listen/<int:pk>', track.by_id, name='track')
]