from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("posts", views.AllPostsView.as_view(), name="posts"),
    path("posts/add", views.AddPostView.as_view(), name="add-post"),
    path("posts/<pk>", views.PostView.as_view(), name="post-detail"),
    path(
        "<first_name>-<last_name>", views.AuthorPostsView.as_view(), name="author-posts"
    ),
]
