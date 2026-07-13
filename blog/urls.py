from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("posts", views.AllPostsView.as_view(), name="posts"),
    path("posts/add", views.AddPostView.as_view(), name="add-post"),
    path("posts/<str:pk>", views.PostView.as_view(), name="post-detail"),
    path("posts/<str:pk>/update", views.UpdatePostView.as_view(), name="post-update"),
    path(
        "<first_name>-<last_name>", views.AuthorPostsView.as_view(), name="author-posts"
    ),
    path("logout", views.logout, name="logout"),
    path("<str:word>", views.notFound),
]
