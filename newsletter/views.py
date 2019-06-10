from django.shortcuts import render
from django.utils.translation import gettext as _
from django.utils.translation import get_language
import globs
import tweepy
from dotenv import load_dotenv
import os
import re
from mx3creations.settings import BASE_DIR
import json
from .forms import NewsletterSubscribeForm
from .models import Member

# Create your views here.
def news(request):
    form = NewsletterSubscribeForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        if get_language() == 'fr':
            lang = 'fr'
        else:
            lang = 'en'
        # if the email isn't taken
        if not Member.objects.filter(email=email).exists():
            form.save(commit=True)
            subscribed = True
        else:
            already_subscribed = True

    load_dotenv(os.path.join(BASE_DIR, '.env'))

    auth = tweepy.OAuthHandler(
        os.getenv('TWITTER_KEY'),
        os.getenv('TWITTER_KEY_SECRET')
    )
    auth.set_access_token(
        os.getenv('TWITTER_TOKEN'),
        os.getenv('TWITTER_TOKEN_SECRET')
    )

    api = tweepy.API(auth)

    raw_tweets = api.user_timeline('mx3_fr', include_entities=True, tweet_mode='extended')
    tweets = list()
    with open(os.path.join(BASE_DIR, 'twapi-response.hidden.json'),'w') as f:
        f.write(json.dumps({idx:tw._json for idx, tw in enumerate(raw_tweets)}, indent=2))

    def fix_links(tweet, links):
        # expand links and add html markup
        for link in links:
            tweet = tweet.replace(link['url'], f"<a class=\"underline\" href=\"{link['expanded_url']}\">{link['expanded_url']}</a>")
        
        # remove junk links (t.co, at the end most of the time)
        bad_urls = re.compile(r'https://t.co/\w{10}')
        for bad_url in bad_urls.findall(tweet):
            tweet = tweet.replace(bad_url, '')
        return tweet

    for tweet in raw_tweets:
        # if the tweet is a response or a retweet, ignore it
        if tweet.retweeted or tweet.full_text.startswith('@'):
            continue

        # removes the link at the end
        rmlnk = re.compile(r'(.+) https?://t.co/\w+$')
        
        data = {
            'url':'https://twitter.com/mx3_fr/status/'+tweet.id_str,
            'text': fix_links(tweet.full_text, tweet._json['entities']['urls']),
        }

        
        try: 
            data['image'] = tweet._json['entities']['media'][0]['media_url']
        except KeyError: 
            if '[news]' not in data['text']:
                continue
      #  except AttributeError:
      #      data['image'] = False
      #  except KeyError:
      #      data['image'] = False
      #  except IndexError:
      #      data['image'] = False

        tweets.append(data)
    print(tweets)
            
    members_count = len(Member.objects.all())
    page_title = globs.page_title(_("News"))
    return render(request, 'news.pug', locals())
