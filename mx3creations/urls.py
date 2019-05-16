"""mx3creations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from corepages import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('newsletter.urls')),
    path('', include('music.urls')),
    path('', include('corepages.urls')),
    path('404', urls.handler404, name='404'),
    path('403', urls.handler403, name='403'),
    path('500', urls.handler500, name='500'),
]

handler404 = 'corepages.views.handler404'
handler403 = 'corepages.views.handler403'
handler500 = 'corepages.views.handler500'

#### TODO LIST ####
# X Contact form CSS
# X Track numbering
# - Track duration
# - Stats page
# - twitter API implementation for "news" page
# - use current website footer style for social medias
# - autoplay feature, use cookies to store preference
# - translations!