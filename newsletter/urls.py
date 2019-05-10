from django.conf.urls import url
from newsletter.views import *

urlpatterns = [
    url(r'^$', news, name='news'),
    url('subscribe', subscribe, name='subscribe')
]