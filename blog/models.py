from django.db import models
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=250, null=True)
    excerpt = models.CharField(max_length=250)
    content = models.CharField(max_length=1000)
    date = models.DateField(auto_now=False, auto_now_add=False)
    slug = models.SlugField(
        default="",
        blank=True,
        null=False,
        db_index=True,
    )

    def get_absolute_url(self):
        return reverse("post-detail", args=[self.slug])

    def __str__(self):
        return self.title
