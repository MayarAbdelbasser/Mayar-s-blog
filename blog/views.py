from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect
from .forms import PostForm
from django.urls import reverse

# from db import posts
from django.template.loader import render_to_string
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Post, Author
from .mixins import JWTRequiredMixin, AuthVerifiedMixin


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


def logout(request):
    del request.session["access_token"]
    del request.session["refresh_token"]
    return HttpResponseRedirect(reverse("index"))


def notFound(request, word):
    return render(request, "notfound.html")


# Create your views here.


class IndexView(AuthVerifiedMixin, TemplateView):
    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = get_posts()[:3]
        context["is_authenticated"] = self.is_Authenticated
        return context


class AllPostsView(AuthVerifiedMixin, ListView):
    template_name = "blog/posts.html"
    model = Post
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_authenticated"] = self.is_Authenticated
        return context


class AllPostsView(AuthVerifiedMixin, ListView):
    template_name = "blog/posts.html"
    model = Post
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_authenticated"] = self.is_Authenticated
        return context


class PostView(AuthVerifiedMixin, DetailView):
    template_name = "blog/post.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_authenticated"] = self.is_Authenticated
        return context


class AuthorPostsView(AuthVerifiedMixin, TemplateView):
    template_name = "blog/author-posts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        first_name = self.kwargs.get("first_name")
        last_name = self.kwargs.get("last_name")
        context["posts"] = get_author_posts(first_name, last_name)
        context["author_name"] = first_name.capitalize() + " " + last_name.capitalize()
        context["is_authenticated"] = self.is_Authenticated
        return context


class AddPostView(JWTRequiredMixin, AuthVerifiedMixin, CreateView):
    form_class = PostForm
    template_name = "blog/add-post.html"
    model = Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_authenticated"] = self.is_Authenticated
        return context

    def get_success_url(self):
        return reverse("post-detail", args=(self.object.pk,))


class UpdatePostView(JWTRequiredMixin, AuthVerifiedMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/add-post.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.kwargs["pk"])

    def form_valid(self, form):
        print(self.object.author.id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_authenticated"] = self.is_Authenticated
        return context

    def get_success_url(self):
        return reverse("post-detail", args=(self.object.pk,))


# def add_post(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)

#         if form.is_valid():
#             user = form.save(commit=False)
#             user.author = Author.objects.all()[0]
#             user.save()
#             return HttpResponseRedirect("/")
#     else:
#         form = PostForm()
#     return render(request, "blog/add-post.html", {"form": form})


# def index(request):
#     posts = get_posts()[:3].values()
#     return render(request, "blog/index.html", {"posts": posts[0:3]})


# def show_posts(request):
#     posts = get_posts().order_by("-date")
#     return render(request, "blog/posts.html", {"posts": posts})


# def show_post(request, slug):
#     try:
#         post = get_post(slug)
#         tags = post.tags.all().values()
#     except:
#         response_data = render_to_string("notfound.html")
#         return HttpResponseNotFound(response_data)

#     return render(request, "blog/post.html", {"post": post, "tags": tags})


# def show_author_posts(request, first_name, last_name):
#     try:
#         posts = get_author_posts(first_name, last_name)
#         author_name = first_name.capitalize() + " " + last_name.capitalize()
#     except:
#         response_data = render_to_string("notfound.html")
#         return HttpResponseNotFound(response_data)

#     return render(
#         request,
#         "blog/author-posts.html",
#         {"author_name": author_name, "posts": posts},
#     )
