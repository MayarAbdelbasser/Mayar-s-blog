from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("", views.getRoutes),
    path("test", views.test_user),
    path("posts", views.getPosts),
    path("posts/create/", views.createPost),
    path("posts/delete/<str:pk>", views.deletePost),
    path("posts/<str:pk>", views.getPost),
    path("users/register/", views.register, name="register"),
    path("users/login/", views.login, name="login"),
    path("users/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("users/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
