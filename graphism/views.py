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
def graphism(request):

    total_size = 0
    for dirpath, dirnames, filenames in os.walk(staticfiles_storage.path(f'static/graphism/images/')):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    page_title = globs.page_title('graphism')
    return render(request, 'graphism.pug', locals())

class View:
    # --- DIFFERENT METHODS ---
    def latest(request):
        img = Image.objects.latest('date')
        return HttpResponseRedirect(reverse('image', kwargs={'title':img.slug}))
    
    def random(request):
        img = Image.random()
        return HttpResponseRedirect(reverse('image', kwargs={'title':img.slug}))

    def by_id(request, pk, play=None):
        img = get_object_or_404(Image, pk=pk)
        return image(request, locals())
    
    def by_title(request, title, play=None):
        img = get_object_or_404(Image, slug=title)
        return image(request, locals())

def image(request, data):

    data.update(locals())
    return render(request, 'image.pug', data)