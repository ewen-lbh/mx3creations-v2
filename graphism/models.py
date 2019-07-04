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

def size_display(dimensions):
    w, h = str(dimensions).split('x')
    return f"{w} px &times; {h} px"

# Create your models here.
class Image(models.Model):

    title = models.CharField("title", max_length=100)
    slug = models.CharField('title slug', max_length=100, unique=True, null=False)
    dimensions = models.CharField("Dimensions (WxH), in pixels", null=True, blank=True, max_length=30)
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

    def size(self):
        if self.dimensions:
            return self.dimensions
        else:
            
            from PIL import Image
            try:
                with Image.open(staticfiles_storage.path(f'static/graphism/images/{self.slug}.png')) as img:
                    w, h = img.size
            # If the file does not exist
            except FileNotFoundError:
                return '0x0'
            dimensions = f'{round(w)}x{round(h)}'
            self.dimensions = dimensions
            self.save()
            return dimensions

    
    def size_display(self):
        return size_display(self.size())

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        SLUG_BLACKLIST = ('random','latest')

        if self.slug in SLUG_BLACKLIST:
            raise Exception(f"Illegal value! {', '.join(SLUG_BLACKLIST)} are reserved slugs.")
        self.slug = slugify(self.title)
        super(Image, self).save()

    class Meta:
        verbose_name = "video"
        verbose_name_plural = "videos"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("video", kwargs={"title": self.slug})
