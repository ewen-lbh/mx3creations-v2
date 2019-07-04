from django.shortcuts import render_to_response, loader, redirect
from globs import render
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.utils.translation import gettext as _
from django.core.mail import send_mail
from music.models import Track, Collection
from newsletter.models import Member, Article
from music.views import Listen
from fuzzywuzzy import process
import globs
import os
from math import floor
import re
from .forms import ContactForm
from mx3creations.settings import STATIC_ROOT, STATIC_URL
# Create your views here.
def home(request):

    proudest_tracks = Track.objects.order_by('-goodness', '-collection__date')[:4]
    proudest = list()
    for track in proudest_tracks:
        proudest.append((track, track.collection))
    page_title = globs.page_title('')
    return render(request, 'home.pug', locals())

def graphism(request):

    page_title = globs.page_title(_("Graphism"))
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

    page_title = globs.page_title(_("Contact"))
    return render(request, 'contact.pug', locals())

def about(request):

    page_title = globs.page_title(_("About"))
    return render(request, 'about.pug', locals())



def search(request, q=None):
    if 'AJAX' in request.POST:
        q = request.POST['q']
        # results count limit per category
        results_count_limit = 4
    else:
        q = q or request.POST['q'] or request.GET['q']
        results_count_limit = False

    search_query = q

    if search_query in ('>allresults'):
        music_tracks = Track.objects.all()
        music_collections = Collection.objects.all()
    
    else:

        # search in collections
        # search similarity threshold
        threshold = 75
        

        def fuzzy_search(Model, field:str, threshold:int=75):
            
            results = list(set([e[0] for e in Model.objects.all().values_list(field)]))
            results = process.extract(q, results)
            results = [e[0] for e in results if e[1] > threshold]
            return results
            

        # get list of strings containing matching artists
        tracks_artists = fuzzy_search(Track, 'artist', threshold)
        # initialize the QuerySet object
        music_tracks = Track.objects.none()
        # for string of the list, "convert" the string to a QuerySet 
        # and merge it to keep a single QuerySet
        for track_artist in tracks_artists:
            music_tracks |= Track.objects.filter(artist=track_artist)
        # repeat this procedure for track titles and collections titles
        tracks_titles = fuzzy_search(Track, 'title', threshold)
        for track_title in tracks_titles:
            music_tracks |= Track.objects.filter(title=track_title)
        collections_titles = fuzzy_search(Collection, 'title', threshold)

        music_collections = Collection.objects.none()
        for collection_title in collections_titles:
            music_collections |= Collection.objects.filter(title=collection_title)
        
    original_results_count = len(music_collections) + len(music_tracks)
    if results_count_limit:
        limit = floor(results_count_limit/2)
        music_collections = music_collections[:limit]
        music_tracks = music_tracks[:limit]
    results_count = len(music_collections) + len(music_tracks)
    more_results_available = original_results_count > results_count

    if 'AJAX' in request.POST:
        return render(request, 'ajax-search.pug', locals())
    else:
        if len(music_tracks) == 1:
            trk = music_tracks.first()
            return redirect('track', title=trk.collection.slug, play=trk.slug)

        if len(music_collections) == 1:
            col = music_collections.first()
            return redirect('track', title=col.slug)

        page_title = globs.page_title(_("Search"))
        return render(request, 'search.pug', locals())

def error_texts(status_code):
    return {
        404: {
            'error_title': _("That's a 404!"),
            'error_description': _("The page you wanted to see does not exist, or has been moved.")
        },
        403: {
            'error_title': _("You shall not pass!"),
            'error_description': _("You don't have access to that page. Try authenticating first.")
        },
        500: {
            'error_title': _("Something's wrong on my end..."),
            'error_description': _("Internal server error. Will be dealing with that «soon» :p")
        }
    }.get(status_code, 500)

def get_error_page(request, status_code):
    return render(request, 'error.pug', error_texts(status_code))

def handler404(request, *args, **kwargs):
    template = loader.get_template('errors.pug')
    response = HttpResponseNotFound(template.render(request=request, context=error_texts(404)))
    return response

def handler403(request, *args, **kwargs):
    template = loader.get_template('errors.pug')
    response = HttpResponseNotFound(template.render(request=request, context=error_texts(403)))
    return response

def handler500(request, *args, **kwargs):
    template = loader.get_template('errors.pug')
    response = HttpResponseNotFound(template.render(request=request, context=error_texts(500)))
    return response

def stats(request):
    music_hours=round(sum([e.duration().seconds for e in Collection.objects.all()]) / 3600, 2)
    music_count=len(Track.objects.all())
    music_albums = len(Collection.objects.filter(kind='AB'))
    music_eps = len(Collection.objects.filter(kind='EP'))
    music_singles = len(Collection.objects.filter(kind='SG'))
    music_remixes = len(Track.objects.filter(is_remix=True))
    # If the video_url field is not empty nor null
    music_videos = len(Track.objects.exclude(video_url__isnull=True).exclude(video_url__exact=''))
    # NOTICE: If we have more or less than 2 cover arts for each collection, this will break
    graphism_covers = len(Collection.objects.all()) * 2
    newsletter_members = len(Member.objects.all())
    coding_repos = 14

    stats = [
        {
            'name':_("Music"),
            'stats': [
                {
                    'value': music_count,
                    'desc': _("Tracks")
                },
                {
                    'value': music_hours,
                    'desc': _("Hours of music")
                },
                {
                    'value': music_videos,
                    'desc': _("Music videos")
                },
                {
                    'value': music_remixes,
                    'desc': _("Remixes")
                },
                {
                    'value': music_albums + music_eps,
                    'desc': _("Albums & EPs")
                },
                {
                    'value': music_singles,
                    'desc': _("Singles")
                },
            ]
        },
        {
            'name': _("Graphism"),
            'stats': [
                {
                    'value': graphism_covers,
                    'desc': _("Cover arts")
                }
            ]
        },
        {
            'name': _("Newsletter"),
            'stats': [
                {
                    'value': newsletter_members,
                    'desc': _("Members")
                }
            ]
        },
        {
            'name': _("Coding"),
            'stats': [
                {
                    'value': coding_repos,
                    'desc': _("Projects on GitHub")
                }
            ]
        }
    ]

    page_title = globs.page_title(_("Statistics"))
    return render(request, 'stats.pug', locals())

def videos(request):


    page_title = globs.page_title(_("Videos"))
    return render(request, 'videos.pug', locals())

def legal(request):



    page_title = 'Legal'
    return render(request, 'legal.pug', {'page_title':globs.page_title(page_title)})

def brand_resources(request):

    
    page_title = globs.page_title(_("Brand resources"))
    return render(request, 'brand_resources.pug', locals())

def coding(request):
    
    
    
    page_title = globs.page_title(_('coding'))
    return render(request, 'coding.pug', locals())