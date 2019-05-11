from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.staticfiles.templatetags.staticfiles import static
from .models import Collection, Track
import os
import corepages
import globs

# Create your views here.
class Listen:
    # --- DIFFERENT METHODS TO GET COLLECTION & (TRACK)
    def latest(request):
        collection = Collection.objects.latest('date')
        tracks = Track.objects.filter(collection__pk=collection.pk)
        return track(request, locals())
    
    def random(request):
        collection = Collection.random()
        tracks = Track.objects.filter(collection__pk=collection.pk)
        return track(request, locals())

    def by_id(request, pk, play=None):
        collection = get_object_or_404(Collection, pk=pk)
        if play:
            play_track = get_object_or_404(Track, pk=play)
        tracks = Track.objects.filter(collection__pk=pk)
        return track(request, locals())
    
    def by_title(request, title, play=None):
        collection = get_object_or_404(Collection, slug=title)
        if play:
            play_track = get_object_or_404(Track, slug=play)
        tracks = Track.objects.filter(collection__slug=title)
        return track(request, locals())

def track(request, data):
    tracks_count = len(data['tracks'])
      
    if tracks_count == 1 and data['tracks'][0].video_url:
        data['collection'].playlist_url = data['tracks'][0].video_url

    # TODO shame !
    btn_array_class = 'quad' if data['collection'].playlist_url else 'tri'

    if tracks_count == 1:
        data['play_track'] = data['tracks'].first()

    # if we don't have a play_track
    if data.get('play_track', None) is None:
        # artist – title kind
        # eg.
        # Mx3 – Patterns EP
        page_title = f"{data['tracks'].first().artist} – {data['collection'].title} {data['collection'].get_kind_display()}"
    else:
        page_title = f"▶ {data['play_track'].artist} – {data['play_track'].title}"

    page_title = globs.page_title(page_title)


    data.update(locals())
    return render(request, 'track.pug', data)

def music(request):
    latest = Collection.objects.latest('date')
    collections = Collection.objects.all()
    page_title = globs.page_title('my music')
    return render(request, 'music.pug', locals())

def cover_art(request, title):
    collection = get_object_or_404(Collection, slug=title)
    page_title = globs.page_title('download cover arts')
    return render(request, 'cover_art.pug', locals())

def share(request, what, item):
    if what == 'collection':
        item = get_object_or_404(Collection, slug=item)
        thing = item.get_kind_display()
        collection = item
    elif what == 'track':
        item = get_object_or_404(Track, slug=item)
        thing = 'track'
        collection = item.collection
    else:
        raise Http404

    page_title = globs.page_title('share')
    return render(request, 'share.pug', locals())