from django.http import Http404
from django.shortcuts import render, get_object_or_404, reverse
from django.utils.timezone import localdate
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
        tracks = Collection.tracks(pk=collection.pk).order_by('track_number')
        return track(request, locals())
    
    def random(request):
        collection = Collection.random()
        tracks = Collection.tracks(pk=collection.pk).order_by('track_number')
        return track(request, locals())

    def by_id(request, pk, play=None):
        collection = get_object_or_404(Collection, pk=pk)
        if play:
            play_track = get_object_or_404(Track, pk=play)
        tracks = Collection.tracks(pk=pk).order_by('track_number')
        return track(request, locals())
    
    def by_title(request, title, play=None):
        collection = get_object_or_404(Collection, slug=title)
        if play:
            play_track = get_object_or_404(Track, slug=play)
        tracks = Collection.tracks(slug=title).order_by('track_number')
        return track(request, locals())

def track(request, data):
    tracks_count = len(data['tracks'])
      
    # fill collection playlist_url with the only track's video url
    if tracks_count == 1 and data['tracks'][0].video_url:
        data['collection'].playlist_url = data['tracks'][0].video_url

    # TODO shame !
    btn_array_class = 'quad' if data['collection'].playlist_url else 'tri'

    # auto-play collections w/ 1 track
    if tracks_count == 1:
        data['play_track'] = data['tracks'].first()

    # set page title
    if data.get('play_track', None) is None:
        # artist – title kind
        # eg.
        # Mx3 – Patterns EP
        page_title = f"{data['tracks'].first().artist} – {data['collection'].title} {data['collection'].get_kind_display()}"
    else:
        # ▶ artist – title
        page_title = f"▶ {data['play_track'].artist} – {data['play_track'].title}"

    # set artist in page if they're all the same (treated in template)
    # Collection.artist returns False if multiple different artists are in the same collection's tracks
    multiple_artists = not Collection.artist(slug=data['collection'].slug)
    print(multiple_artists)

    page_title = globs.page_title(page_title)
    data.update(locals())
    return render(request, 'track.pug', data)

def music(request, sort='date'):
    latest = Collection.objects.latest('date')
    collections = Collection.objects.all()
    page_title = globs.page_title('my music')

    sort_options = [
        ('date', 'Date'),
        ('goodness', 'Goodness'),
        ('kind', 'Kind'),
        ('work-time', 'Work time'),
    ]

    print(collections)


    def goodness_sort(collection):
        goodness = Collection.goodness(slug=collection.slug)
        print(goodness, collection.slug)
        return goodness

    if sort == 'goodness':
        collections = sorted(collections, reverse=True, key=goodness_sort)
        
        print(collections)

    elif sort == 'date':
        collections = collections.order_by('-date')
        print(collections)
    elif sort == 'kind':
        collections = {
            'EP': collections.filter(kind='EP').order_by('-date'),
            'AB': collections.filter(kind='AB').order_by('-date'),
            'SG': collections.filter(kind='SG').order_by('-date')
        }
    elif sort == 'work-time':
        collections = collections.order_by('-work_time')
    else:
        collections = collections.order_by(sort)

    return render(request, 'music.pug', locals())

def cover_art(request, title):
    collection = get_object_or_404(Collection, slug=title)
    page_title = globs.page_title('download cover arts')
    return render(request, 'cover_art.pug', locals())

def share(request, what, item):
    if what == 'collection':
        item = get_object_or_404(Collection, slug=item)
        collection = item
        thing = item.get_kind_display()
        artist = Collection.artist(slug=item)
        print(artist)

    elif what == 'track':
        item = get_object_or_404(Track, slug=item)
        thing = 'track'
        collection = item.collection
        artist = item.artist

    else:
        raise Http404

    share_url_params = {
        'title': collection.slug,
    }
    if what == 'track':
        share_url_params['play'] = item.slug
    
    share_url = reverse('track', args=share_url_params)
    share_title = f'"{item.title}" {"by " + artist if artist else ""}'

    page_title = globs.page_title('share')
    return render(request, 'share.pug', locals())


def addallfolders():
    DIR = '/home/ewen/Coding/projects/mx3creations/static/music/audio/'
    for collection in Collection.objects.all():
        foldername = collection.slug
        os.mkdir(DIR+foldername)

if __name__ == "__main__":
    addallfolders()