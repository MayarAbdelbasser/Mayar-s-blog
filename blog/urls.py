from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("posts", views.show_posts, name="posts"),
    path("posts/<slug>", views.show_post, name="post-detail"),
]
