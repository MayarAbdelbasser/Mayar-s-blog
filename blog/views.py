from django.shortcuts import render
from django.http import HttpResponseNotFound
from db import posts
from django.template.loader import render_to_string


# Create your views here.
def index(request):
    return render(request, "blog/index.html", {"posts": posts[0:3]})


def show_posts(request):
    return render(request, "blog/posts.html", {"posts": posts})


def show_post(request, slug):
    context = {"post": None}

    try:
        context["post"] = next(post for post in posts if post["id"] == int(slug))
    except:
        response_data = render_to_string("notfound.html")
        return HttpResponseNotFound(response_data)

    return render(request, "blog/post.html", context)
