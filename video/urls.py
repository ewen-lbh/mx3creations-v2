from django.urls import path
from video.views import *

urlpatterns = [
    path('videos/', videos, name='video'),
    path('videos/<slug:sort>', videos, name='video'),

    path('watch/random/', Watch.random, name='video_random'),
    path('watch/latest/', Watch.latest, name='video_latest'),
    path('watch/<slug:title>/', Watch.by_title, name='video'),
    path('watch/<int:pk>/', Watch.by_id, name='video'),
]