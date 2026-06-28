from django.shortcuts import render
from django.http import HttpResponseNotFound

# from db import posts
from django.template.loader import render_to_string
from .models import Post


def get_posts():
    posts = Post.objects.all()
    return posts


def get_post(slug):
    post = Post.objects.filter(slug=slug)
    return post[0]


# Create your views here.
def index(request):
    posts = get_posts().order_by("-date")[0:3]
    return render(request, "blog/index.html", {"posts": posts[0:3]})


def show_posts(request):
    posts = get_posts().order_by("-date")
    return render(request, "blog/posts.html", {"posts": posts})


def show_post(request, slug):
    try:
        post = get_post(slug)
        tags = post.tags.all().values()
    except:
        response_data = render_to_string("notfound.html")
        return HttpResponseNotFound(response_data)

    return render(request, "blog/post.html", {"post": post, "tags": tags})
