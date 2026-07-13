from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator, MinLengthValidator
from django.utils.text import slugify

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


# to change the default user from User model to Author model
class AuthorManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save(using=self._db)
        return user


class Tag(models.Model):
    caption = models.CharField(max_length=50)

    def __str__(self):
        return self.caption


class Author(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(
        max_length=254,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$",
                message="Enter a valid email",
                code="invalid-email",
            )
        ],
    )
    password = models.CharField(max_length=128, null=True)

    objects = AuthorManager()

    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def full_name(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

    def get_absolute_url(self):
        return reverse(
            "author-posts",
            kwargs={"first_name": self.first_name, "last_name": self.last_name},
        )

    def __str__(self):
        return self.full_name()


class Post(models.Model):
    title = models.CharField(max_length=250)
    excerpt = models.CharField(max_length=250)
    content = models.TextField(validators=[MinLengthValidator(10)])
    date = models.DateField(auto_now=False, auto_now_add=True)
    slug = models.SlugField(
        default="", blank=True, null=False, db_index=True, unique=True, primary_key=True
    )
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to="images", null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post-detail", args=[self.slug])

    def __str__(self):
        return self.title
