from django.shortcuts import render
import globs
from .forms import NewsletterSubscribeForm
from .models import Member

# Create your views here.
def news(request):
    
    members_count = len(Member.objects.all())
    page_title = globs.page_title('news')
    return render(request, 'news.pug', locals())

def subscribe(request):
    form = NewsletterSubscribeForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        lang  = form.cleaned_data['lang']
        # if the email isn't taken
        if not Member.objects.filter(email=email).exists():
            form.save(commit=True)
            subscribed = True
        else:
            already_subscribed = True

    page_title = globs.page_title('subscribe')
    # print(page_title)
    return render(request, 'subscribe.pug', locals())
