from django.urls import path
from coding.views import *

urlpatterns = [
    path('coding/', coding, name='coding'),
    path('coding/<slug:sort>', coding, name='coding'),
    
    path('project/random/', Project.random, name='project_random'),
    path('project/latest/', Project.latest, name='project_latest'),
    path('project/<slug:title>/', Project.by_title, name='project'),
    path('project/<int:pk>/', Project.by_id, name='project'),
]