from django.shortcuts import render
from django.http import HttpResponse
from db import posts


# Create your views here.
def index(request):
    return render(request, "blog/index.html", {"posts": posts})


def show_posts(request):
    return render(request, "blog/posts.html", {"posts": posts})


def show_post(request, slug):
    return HttpResponse("post")
