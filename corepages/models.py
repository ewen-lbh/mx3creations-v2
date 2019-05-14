from django.db import models

# Create your models here.
class Connection(models.Model):

    IP = models.CharField("IP Adress", max_length=50)
    # Location = 

    class Meta:
        verbose_name = "connection"
        verbose_name_plural = "connections"

    def __str__(self):
        return self.IP

    def get_absolute_url(self):
        return reverse("connection_detail", kwargs={"pk": self.pk})