from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponse
import globs
# Create your views here.
def home(request):
           
    page_title = ''
    return render(request, 'home.pug', {'page_title':globs.page_title(page_title)})

def music(request):
          
    page_title = 'music'
    return render(request, 'music.pug', {'page_title':globs.page_title(page_title)})

def graphism(request):
      
    page_title = 'graphism'
    return render(request, 'graphism.pug', {'page_title':globs.page_title(page_title)})

def contact(request):
           
    page_title = 'contact'
    return render(request, 'contact.pug', {'page_title':globs.page_title(page_title)})

def about(request):
            
    page_title = 'about'
    return render(request, 'about.pug', {'page_title':globs.page_title(page_title)})

def search(request):
    # search page
    results = ['some','db','magic']
    page_title = 'Search'
    return render(request, 'search.pug', {'search_query':request.GET['q'], 'results_count':len(results), 'results':results, 'page_title':globs.page_title(page_title)})

def handler404(request, *args, **kwargs):
    
    response = render_to_response(request, '404.pug')
    response.status_code = 404
    return response 