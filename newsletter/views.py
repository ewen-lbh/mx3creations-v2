from django.shortcuts import render
import globs
from .forms import NewsletterSubscribeForm
from .models import Member

# Create your views here.
def news(request):
    form = NewsletterSubscribeForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        lang = 'en'  # TODO implement lang detection
        # if the email isn't taken
        if not Member.objects.filter(email=email).exists():
            form.save(commit=True)
            subscribed = True
        else:
            already_subscribed = True
            
    members_count = len(Member.objects.all())
    page_title = globs.page_title('News')
    return render(request, 'news.pug', locals())
