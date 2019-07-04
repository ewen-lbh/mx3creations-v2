import django
import os
from datetime import datetime, timedelta
import json
from mx3creations import settings
from django.contrib.staticfiles.storage import staticfiles_storage

def page_title(title):
    sep = ' • ' if len(title) else ''
    return f"{title}{sep}Mx3's Creations"
    
def render(request, template_name, context=None, content_type=None, status=None, using=None):
    iconsdict = dict()
    for icon in os.listdir(staticfiles_storage.path('static/corepages/images/icons')):
        if not icon.endswith(".svg"):
            continue
        
        name = os.path.splitext(icon)[0]
        with open(os.path.abspath(os.path.join('static/corepages/images/icons', icon)), 'r') as f:
            content = f.read().replace('\n','').replace('  ','')
        iconsdict[name] = content

    if context is None:
        context = dict()
    else:
        context.update({'icons':iconsdict})
    
    return django.shortcuts.render(request, template_name, context, content_type, status, using)

def use_cache(api_name:str) -> list:
    cachefile_path = os.path.join(settings.BASE_DIR, 'cache', f'{api_name}-api.jsonc')

    if os.path.isfile(cachefile_path):
        with open(cachefile_path, 'r') as file: raw=file.read()
        cache_timedelta_raw = float(raw.splitlines()[0].replace('//CACHE_DATE=',''))
        cache_timedelta = datetime.now() - datetime.fromtimestamp(cache_timedelta_raw)
        cache_timedelta_hours = cache_timedelta.total_seconds() / 3600
    else:
        cache_timedelta_hours = settings.API_CACHE_EXPIRATION_HOURS + 1
    
    if cache_timedelta_hours < settings.API_CACHE_EXPIRATION_HOURS:
        projects = json.loads(''.join(raw.splitlines()[1:]))
        print('using cache ^^')
        return projects
    else:
        print(f'Cache too old >< ({cache_timedelta_hours})')
        return None

def write_cache(api_name:str, data) -> list:

    cachefile_path = os.path.join(settings.BASE_DIR, 'cache', f'{api_name}-api.jsonc')
    with open(cachefile_path, 'w', encoding='utf8') as file:
        now = datetime.now().timestamp()
        file.write(f'//CACHE_DATE={now}\n'+json.dumps(data))