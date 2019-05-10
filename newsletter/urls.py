from django.conf.urls import url
from newsletter.views import *

urlpatterns = [
    url(r'^$', news),
    url('subscribe', subscribe)
]