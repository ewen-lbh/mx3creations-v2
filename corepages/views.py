from django.shortcuts import render, render_to_response, loader
from django.http import Http404, HttpResponse, HttpResponseNotFound
import globs
# Create your views here.
def home(request):
           
    page_title = ''
    return render(request, 'home.pug', locals())

def graphism(request):
      
    page_title = globs.page_title('graphism')
    return render(request, 'graphism.pug', locals())

def contact(request):
           
    page_title = globs.page_title('contact')
    return render(request, 'contact.pug', locals())

def about(request):
            
    page_title = globs.page_title('about')
    return render(request, 'about.pug', locals())

def search(request):
    # search page
    results = ['some','db','magic']
    page_title = globs.page_title('Search')
    # return render(request, 'search.pug', {'search_query':request.GET['q'], 'results_count':len(results), 'results':results, 'page_title':globs.page_title(page_title)})
    return render(request, '404.pug')

def handler404(request, *args, **kwargs):
    template = loader.get_template('404.pug')
    response = HttpResponseNotFound(template.render(request=request))
    return response

def stats(request):
    
    page_title = 'stats'
    return render(request, 'stats.pug', {'page_title':globs.page_title(page_title)})

def legal(request):
    
    
    
    page_title = 'legal'
    return render(request, 'legal.pug', {'page_title':globs.page_title(page_title)})