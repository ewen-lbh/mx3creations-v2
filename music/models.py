from django.db import models
from django.shortcuts import reverse
from django.utils import timezone

# Create your models here.
class Track(models.Model):

    title = models.CharField("Track title", max_length=100)
    artist = models.CharField("Artist", max_length=50, default="Mx3")
    is_remix = models.BooleanField("The track is a remix ?")
    duration = models.DurationField("Track duration")
    work_time = models.DurationField("Work time", null=True)
    collection = models.ForeignKey("music.Collection", verbose_name="Track's collection", on_delete=models.CASCADE)
    video_url = models.CharField("YouTube video URL", max_length=100, null=True)

    class Meta:
        verbose_name = "track"
        verbose_name_plural = "tracks"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("track_detail", kwargs={"pk": self.pk})

    def duration(self):
        return 

class Collection(models.Model):

    KINDS = (
        ("EP","EP"),
        ("SG","Single"),
        ("AB","Album")
    )

    title = models.CharField("Collection title", max_length=100)
    cover_color = models.CharField("Cover art's color dominant", max_length=5)
    kind = models.CharField("Kind/type", max_length=6, choices=KINDS)
    date = models.DateField("Date published", default=timezone.now)

    class Meta:
        verbose_name = "collection"
        verbose_name_plural = "collections"

    def __str__(self):
        return self.title

    def duration(self):
        return sum()

    def get_absolute_url(self):
        return reverse("collection_detail", kwargs={"pk": self.pk})
