from django.urls import path
from graphism.views import *

urlpatterns = [
    path('graphism/', graphism, name='graphism'),
    path('graphism/<slug:sort>', graphism, name='graphism'),

    path('view/random/', View.random, name='image_random'),
    path('view/latest/', View.latest, name='image_latest'),
    path('view/<slug:title>/', View.by_title, name='image'),
    path('view/<int:pk>/', View.by_id, name='image'),
]