from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("posts", views.show_posts, name="posts"),
    path("add-post", views.add_post, name="add-post"),
    path("posts/<slug>", views.show_post, name="post-detail"),
    path("<first_name>-<last_name>", views.show_author_posts, name="author-posts"),
]
