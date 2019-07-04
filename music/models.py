from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.translation import get_language
from . import vibrant
import datetime
from markdown import markdown
from html2text import html2text

def duration_display(timedelta):
    h, m, s = str(timedelta).split(':')
    hours = '{:02}:'.format(int(h)) if int(h) else ''
    rest = '{:02}\'{:02}"'.format(int(m), int(s))
    return f"{hours}{rest}"


# Create your models here.
class Track(models.Model):

    title = models.CharField("Track title", max_length=100)
    slug = models.CharField('Track title slug', max_length=100, unique=True, null=False)
    artist = models.CharField("Artist", max_length=50, default="Mx3")
    is_remix = models.BooleanField("The track is a remix ?")
    length = models.DurationField("Track duration", null=True, blank=True)
    goodness = models.IntegerField("Goodness /20", default=10, validators=[MaxValueValidator(20), MinValueValidator(0)])
    collection = models.ForeignKey("music.Collection", verbose_name="Track's collection", on_delete=models.CASCADE)
    video_url = models.CharField("YouTube video URL", max_length=100, blank=True, null=True)
    track_number = models.IntegerField("Track number", validators=[MinValueValidator(1)], null=False, default=1)
    downloads = models.IntegerField("Downloads count", validators=[MinValueValidator(0)], default=0)
    likes = models.IntegerField("Likes count", validators=[MinValueValidator(0)], default=0)

    # dynamically create the slug & set the duration
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super(Track, self).save()

    class Meta:
        verbose_name = "track"
        verbose_name_plural = "tracks"

    def __str__(self):
        return f"{self.artist} - {self.title}"

    def get_absolute_url(self):
        return reverse("track", kwargs={"title": self.collection.slug, "play":self.slug})

    def duration(self):
        if self.length:
            return self.length
        else:
            
            from mutagen.mp3 import MP3
            from mutagen import MutagenError
            try:
                audio = MP3(staticfiles_storage.path(f'static/music/audio/{self.collection.slug}/{self.slug}.mp3'))
            # If the file does not exist
            except MutagenError:
                return datetime.timedelta(seconds=0)
            duration = round(audio.info.length)
            duration = datetime.timedelta(seconds=duration)
            self.length = duration
            self.save()
            return duration

    def duration_display(self):
        return duration_display(self.duration())

    def track_number_display(self):
        highestlen = len(str(len(self.collection.tracks())))
        
        tracknum = self.track_number
        tracknum = tracknum if tracknum is not None else '??'
        return "{:0>{w}}".format(str(tracknum), w=highestlen)

class Collection(models.Model):

    KINDS = (
        ("EP","EP"),
        ("SG","single"),
        ("AB","album")
    )

    COVER_COLORS = (
        ("D","Dark"),
        ("L","Light")
    )


    title = models.CharField("Collection title", max_length=100)
    slug = models.CharField('Collection title slug', max_length=100, unique=True, null=False)
    work_time = models.DurationField("Work time", null=True, blank=True)
    description_fr = models.TextField("Description (fr)", null=True, blank=True)
    description_en = models.TextField("Description (en)", null=True, blank=True)
    cover_color = models.CharField("Cover art's color dominant (dark or light)", max_length=5, choices=COVER_COLORS)
    cover_accent_color = models.CharField("Cover art's accent color", blank=True, null=True, max_length=12)
    playlist_url = models.CharField("YouTube playlist URL", max_length=200, null=True, blank=True)
    kind = models.CharField("Kind/type", max_length=6, choices=KINDS)
    date = models.DateField("Date published", default=timezone.now)

    # dynamically create the slug
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        SLUG_BLACKLIST = ('random','latest')

        if self.slug in SLUG_BLACKLIST:
            raise Exception(f"Illegal value! {', '.join(SLUG_BLACKLIST)} are reserved slugs.")
        self.slug = slugify(self.title)
        super(Collection, self).save()

    class Meta:
        verbose_name = "collection"
        verbose_name_plural = "collections"

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("track", kwargs={"title": self.slug})


    def duration(self):
        duration = sum([
            e.duration().seconds for e in Track.objects.filter(collection__slug=self.slug)
        ])
        return datetime.timedelta(seconds=duration)

    def duration_display(self):
        return duration_display(self.duration())

    def random():
        # NOTICE: This might be the cause of slow DB operations
        collection = Collection.objects.order_by('?').first()
        return collection

    def tracks(self):
        return Track.objects.filter(collection__slug=self.slug).order_by('track_number')
    
    def artist(self, single_artist=True):
        artists = self.tracks()
        
        #dedupe list
        artists = list(set(artists))

        if len(artists) == 1:
            return artists[0]
        else:
            if single_artist:
                return False
            else:
                return ', '.join(artists)

    def goodness(self):
        tracks = self.tracks()
        return 1/len(tracks) * sum([track.goodness for track in tracks])

    def get_total(slug, what):
        return sum([getattr(e, what) for e in tracks(slug)])

    def description_markdown(self):
        if get_language() == 'fr':
            return self.description_fr
            
        else:
            return self.description_en
            
    def description_plain(self):
        return html2text(self.description_html())
    def description_html(self):
        html = markdown(self.description_markdown())
        html = html.replace('<p>','').replace('</p>','')
        html = html.replace('<a ', '<a target="_blank" ')
        return html

    def accent_color(self):
        if not self.cover_accent_color:
            image = staticfiles_storage.path(f'static/music/images/wide/{self.slug}.jpg')
            color = vibrant.mostvibrant_palette(image)
            self.cover_accent_color = color
            self.save()

        return self.cover_accent_color
