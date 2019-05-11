from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Track(models.Model):

    title = models.CharField("Track title", max_length=100)
    slug = models.CharField('Track title slug', max_length=100, unique=True, null=False)
    artist = models.CharField("Artist", max_length=50, default="Mx3")
    is_remix = models.BooleanField("The track is a remix ?")
    duration = models.DurationField("Track duration")
    goodness = models.IntegerField("Goodness /20", default=10, validators=[MaxValueValidator(20), MinValueValidator(0)])
    collection = models.ForeignKey("music.Collection", verbose_name="Track's collection", on_delete=models.CASCADE)
    video_url = models.CharField("YouTube video URL", max_length=100, blank=True, null=True)
    #date = models.DateField("Date published", default="<<<<<Je voudrais le field 'date' de la Collection liée>>>>>")

    # dynamically create the slug
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super(Track, self).save()

    class Meta:
        verbose_name = "track"
        verbose_name_plural = "tracks"

    def __str__(self):
        return f"{self.artist} - {self.title}"

    def get_absolute_url(self):
        return reverse("track_detail", kwargs={"pk": self.pk})

    def duration(self):
        # duration = get_duration(audio_filename(title=self.title, collection=self.collection.title))
        # if not Track.objects.get(pk=self.pk).duration:
        #     self.duration = duration
        return 

class Collection(models.Model):

    KINDS = (
        ("EP","EP"),
        ("SG","Single"),
        ("AB","Album")
    )

    COVER_COLORS = (
        ("D","Dark"),
        ("L","Light")
    )

    SLUG_BLACKLIST = ('random','latest')

    title = models.CharField("Collection title", max_length=100)
    slug = models.CharField('Collection title slug', max_length=100, unique=True, null=False)
    work_time = models.DurationField("Work time", null=True, blank=True)
    cover_color = models.CharField("Cover art's color dominant", max_length=5, choices=COVER_COLORS)
    playlist_url = models.CharField("YouTube playlist URL", max_length=200, null=True, blank=True)
    kind = models.CharField("Kind/type", max_length=6, choices=KINDS)
    date = models.DateField("Date published", default=timezone.now)

    # dynamically create the slug
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.slug in SLUG_BLACKLIST:
            raise Exception(f"Illegal value! {','.join(SLUG_BLACKLIST)} are reserved slugs.")
        self.slug = slugify(self.title)
        super(Collection, self).save()

    class Meta:
        verbose_name = "collection"
        verbose_name_plural = "collections"

    def __str__(self):
        return self.title

    def duration(self):
        return
        #return sum("<<<<<ici je veux avoir la somme des fields duration de chaque Track lié à cette Collection>>>>>")

    def random():
        # NOTICE: This might be the cause of slow DB operations
        collection = Collection.objects.order_by('?').first()
        return collection