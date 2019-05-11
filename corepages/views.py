from django.shortcuts import render, render_to_response, loader, redirect
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.core.mail import send_mail
from music.models import Track, Collection
from music.views import Listen
import globs
import re
from .forms import ContactForm
# Create your views here.
def home(request):
    proudest_tracks = Track.objects.order_by('-goodness', '-collection__date')[:5]
    proudest = list()
    for track in proudest_tracks:
        proudest.append((track, track.collection))
    page_title = globs.page_title('')
    return render(request, 'home.pug', locals())

def graphism(request):
    
    page_title = globs.page_title('graphism')
    return render(request, 'graphism.pug', locals())

def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        try:
            send_mail(
                # subject
                f'[mx3creations] Contact from {form.cleaned_data["email"]}',
                # body
                form.cleaned_data['message'],
                # from email
                form.cleaned_data['email'],
                # to email
                ('ewen.lebihan7@gmail.com', )
            )
            sent = True
        except Exception as e:
            sent = False
            regex = re.compile(r'\[.+\](.+)')
            send_error = regex.sub(r'\1', str(e)) + " :/"
    
    page_title = globs.page_title('contact')
    return render(request, 'contact.pug', locals())

def about(request):
            
    page_title = globs.page_title('about')
    return render(request, 'about.pug', locals())

def search(request):
    # search page
    search_query = q = request.GET['q']

    # search in collections
    collections_by_titles = Collection.objects.filter(title__icontains=q)
    collections_by_kind = Collection.objects.filter(kind__icontains=q)
    collections = collections_by_kind | collections_by_titles

    # search in individual tracks
    tracks_by_artist = Track.objects.filter(artist__icontains=q)
    tracks_by_title = Track.objects.filter(title__icontains=q)
    tracks = tracks_by_artist | tracks_by_title

    # if there's only one result, redirect

    if len(tracks) == 1:
        trk = tracks.first()
        return redirect('track', title=trk.collection.slug, play=trk.slug)

    if len(collections) == 1:
        col = collections.first()
        return redirect('track', title=col.slug)
    
    results_count = len(collections) + len(tracks)
    page_title = globs.page_title('Search')
    return render(request, 'search.pug', locals())

def handler404(request, *args, **kwargs):
    template = loader.get_template('404.pug')
    response = HttpResponseNotFound(template.render(request=request))
    return response

def handler403(request, *args, **kwargs):
    template = loader.get_template('403.pug')
    response = HttpResponseForbidden(template.render(request=request))
    return response

def handler500(request, *args, **kwargs):
    template = loader.get_template('500.pug')
    response = HttpResponseServerError(template.render(request=request))
    return response

def stats(request):
    
    page_title = 'stats'
    return render(request, 'stats.pug', {'page_title':globs.page_title(page_title)})

def legal(request):
    
    
    
    page_title = 'legal'
    return render(request, 'legal.pug', {'page_title':globs.page_title(page_title)})