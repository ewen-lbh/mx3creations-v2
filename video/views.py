from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, reverse
from django.utils.translation import gettext as _
from django.utils.timezone import localdate
from django.contrib.staticfiles.templatetags.staticfiles import static
from .models import *
import os
import corepages
import time
import globs
from globs import render

# Create your views here.
def videos(request):
    total_hours = sum([v.duration().total_seconds() / 3600 for v in Video.objects.all()])
    page_title = globs.page_title('videos')
    return render(request, 'videos.pug', locals())

class Watch:
    # --- DIFFERENT METHODS ---
    def latest(request):
        vid = Video.objects.latest('date')
        return HttpResponseRedirect(reverse('video', kwargs={'title':vid.slug}))
    
    def random(request):
        vid = Video.random()
        return HttpResponseRedirect(reverse('video', kwargs={'title':vid.slug}))

    def by_id(request, pk, play=None):
        vid = get_object_or_404(Video, pk=pk)
        return video(request, locals())
    
    def by_title(request, title, play=None):
        vid = get_object_or_404(Video, slug=title)
        return video(request, locals())

def video(request, data):

    data.update(locals())
    return render(request, 'video.pug', data)