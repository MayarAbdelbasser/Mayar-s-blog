from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator


# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField(
        max_length=254,
        validators=[
            RegexValidator(
                regex=r"((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$",
                message="Enter a valid email",
                code="invalid-email",
            )
        ],
    )

    def full_name(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

    def __str__(self):
        return self.full_name()


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
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse("post-detail", args=[self.slug])

    def __str__(self):
        return self.title
