from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, reverse
from django.utils.translation import gettext as _
from django.utils.timezone import localdate
from django.contrib.staticfiles.templatetags.staticfiles import static
from mx3creations import settings
from datetime import datetime, timedelta
from .models import *
import os
import corepages
import time
import globs
import json
import requests
from globs import render

# Create your views here.
def coding(request):
    
    projects = globs.use_cache('github')
    
    if projects is None:
        repos = requests.get('https://api.github.com/users/ewen-lbh/repos').json()
        pinned_repos = requests.get('https://gh-pinned-repos.now.sh/?username=ewen-lbh').json()
        pinned_repos_names = [r['repo'] for r in pinned_repos]
        projects = list()
        
        for repo in repos:
            if repo['fork']: continue
            # print(repo, end="\n\n\n")
            project = {
                "url": repo['html_url'],
                "description": repo['description'],
                "name": repo['name'],
                "full_name": repo['full_name'],
                "creation": repo['created_at'],
                "update": repo['updated_at'],
                # "license": repo['license']['name'],
                # "license_url": repo['license']['url'],
                "pinned": repo['name'] in pinned_repos_names
            }
            projects.append(project)
        
        globs.write_cache('github', projects)


    page_title = globs.page_title('coding')
    return render(request, 'coding.pug', locals())

class Project:
    # --- DIFFERENT METHODS ---
    def latest(request):
        proj = dict()
        return HttpResponseRedirect(reverse('project', kwargs={'title':proj.slug}))
    
    def random(request):
        proj = dict()
        return HttpResponseRedirect(reverse('project', kwargs={'title':proj.slug}))

    def by_id(request, pk, play=None):
        proj = dict()
        return project(request, locals())
    
    def by_title(request, title, play=None):
        proj = dict()
        return project(request, locals())

def project(request, data):

    data.update(locals())
    return render(request, 'project.pug', data)