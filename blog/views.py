from django.shortcuts import render
from django.http import HttpResponseNotFound

# from db import posts
from django.template.loader import render_to_string
from .models import Post


def get_posts():
    posts = Post.objects.all().values()
    return posts


def get_post(slug):
    post = Post.objects.filter(slug=slug).values()
    return post[0]


# Create your views here.
def index(request):
    posts = get_posts()
    return render(request, "blog/index.html", {"posts": posts[0:3]})


def show_posts(request):
    return render(request, "blog/posts.html", {"posts": posts})


def show_post(request, slug):
    try:
        post = get_post(slug)
    except:
        response_data = render_to_string("notfound.html")
        return HttpResponseNotFound(response_data)

    return render(request, "blog/post.html", {"post": post})
