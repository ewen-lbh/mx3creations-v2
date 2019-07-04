from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.translation import get_language
import datetime
from markdown import markdown
from html2text import html2text


def duration_display(timedelta):
    h, m, s = str(timedelta).split(':')
    hours = '{:02}:'.format(int(h)) if int(h) else ''
    rest = '{:02}\'{:02}"'.format(int(m), int(s))
    return f"{hours}{rest}"


# Create your models here.
class Video(models.Model):

    title = models.CharField("title", max_length=100)
    slug = models.CharField('title slug', max_length=100, unique=True, null=False)
    length = models.DurationField("Duration", null=True, blank=True)
    kind = models.CharField(max_length=100)
    date = models.DateField("Date published", default=timezone.now)
    description_fr = models.TextField("Description (fr)", null=True, blank=True)
    description_en = models.TextField("Description (en)", null=True, blank=True)
    downloads = models.IntegerField("Downloads count", validators=[MinValueValidator(0)], default=0)
    likes = models.IntegerField("Likes count", validators=[MinValueValidator(0)], default=0)


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

    def duration(self):
        if self.length:
            return self.length
        else:
            
            from mutagen.mp4 import MP4
            from mutagen import MutagenError
            try:
                video = MP4(staticfiles_storage.path(f'static/video/video/{self.slug}.mp4'))
            # If the file does not exist
            except MutagenError:
                return datetime.timedelta(seconds=0)
            duration = round(video.info.length)
            duration = datetime.timedelta(seconds=duration)
            self.length = duration
            self.save()
            return duration

    def duration_display(self):
        return duration_display(self.duration())

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        SLUG_BLACKLIST = ('random','latest')

        if self.slug in SLUG_BLACKLIST:
            raise Exception(f"Illegal value! {', '.join(SLUG_BLACKLIST)} are reserved slugs.")
        self.slug = slugify(self.title)
        super(Video, self).save()

    class Meta:
        verbose_name = "video"
        verbose_name_plural = "videos"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("video", kwargs={"title": self.slug})
