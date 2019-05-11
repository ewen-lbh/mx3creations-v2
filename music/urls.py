from django.urls import path
from music.views import *

urlpatterns = [
    path('music', music, name='music'),
    
    path('listen/random', Listen.random, name='track_random'),
    path('listen/latest', Listen.latest, name='track_latest'),
    path('listen/<slug:title>', Listen.by_title, name='track'),
    path('listen/<int:pk>', Listen.by_id, name='track'),
    path('listen/<slug:title>/<slug:play>', Listen.by_title, name='track'),
    path('listen/<int:pk>/<int:play>', Listen.by_id, name='track'),

    path('share/<slug:what>/<slug:item>', share, name='share'),
    path('cover-art/<slug:title>', cover_art, name='cover_art'),

]