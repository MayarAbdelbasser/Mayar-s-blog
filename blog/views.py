from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect
from .forms import PostForm

# from db import posts
from django.template.loader import render_to_string
from .models import Post, Author


def get_posts():
    posts = Post.objects.all().order_by("-date")
    return posts


def get_post(slug):
    post = Post.objects.filter(slug=slug)
    return post[0]


def get_author_posts(first_name, last_name):
    author = Author.objects.get(first_name=first_name, last_name=last_name)
    posts = author.posts.all()
    return posts


# Create your views here.
def index(request):
    posts = get_posts()[:3].values()
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


def show_author_posts(request, first_name, last_name):
    try:
        posts = get_author_posts(first_name, last_name)
        author_name = first_name.capitalize() + " " + last_name.capitalize()
    except:
        response_data = render_to_string("notfound.html")
        return HttpResponseNotFound(response_data)

    return render(
        request,
        "blog/author-posts.html",
        {"author_name": author_name, "posts": posts},
    )


def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.author = Author.objects.all()[0]
            user.save()
            return HttpResponseRedirect("/")
    else:
        form = PostForm()
    return render(request, "blog/add-post.html", {"form": form})


def notfound(request, random):
    try:
        int("hello")
    except:
        response_data = render_to_string("notfound.html")
        return HttpResponseNotFound(response_data)
