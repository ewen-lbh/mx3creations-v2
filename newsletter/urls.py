from django.urls import path
from newsletter.views import *

urlpatterns = [
    path('', news, name='news'),
]