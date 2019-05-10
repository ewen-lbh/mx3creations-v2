from django.shortcuts import render
from .models import Collection, Track
import corepages
import globs

# Create your views here.
class track:
    @staticmethod
    def by_id(request, id):
        return corepages.views.handler404(request)
    
    @staticmethod
    def by_title(request, title):
        return corepages.views.handler404(request)

def music(request):
    latest = Collection.objects.latest('date')
    latest_kind = latest.get_kind_display()
    collections = Collection.objects.all()
    page_title = globs.page_title('my music')
    return render(request, 'music.pug', locals())

# NOT VIEWS
def get_latest():
    # latest page
    # get track infos here
    track = "some db magic"
    return track

def get_random():
    track = "some db magic"
    return track