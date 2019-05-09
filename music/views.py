from django.shortcuts import render
import corepages

# Create your views here.
def get_latest():
    # latest page
    # get track infos here
    track = "some db magic"
    return track

def get_random():
    track = "some db magic"
    return track

class track:
    @staticmethod
    def by_id(request, id):
        return corepages.views.handler404(request)
    
    @staticmethod
    def by_title(request, title):
        return corepages.views.handler404(request)