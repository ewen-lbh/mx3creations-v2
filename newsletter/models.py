from django.shortcuts import reverse
from django.db import models

# Create your models here.
class Member(models.Model):
    LANGUAGES = (
        ('fr','French'),
        ('en','English')
    )
    email = models.EmailField("Email", max_length=254)
    lang  = models.CharField("Language", max_length=20, choices=LANGUAGES)

    class Meta:
        verbose_name = "Member"
        verbose_name_plural = "Members"

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("Member_detail", kwargs={"pk": self.pk})

class Article(models.Model):

    title = models.CharField("Title", max_length=50)
    body = models.TextField("Article body")

    class Meta:
        verbose_name = "article"
        verbose_name_plural = "articles"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"pk": self.pk})
