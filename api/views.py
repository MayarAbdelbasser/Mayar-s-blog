from .serializers import PostSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from blog.models import Post


# specify request method
@api_view(["GET"])
def getRoutes(request):
    routes = [{"GET": "/api/"}, {"GET": "/api/posts/slug"}, {"POST": "/api/posts"}]
    return Response(routes)


@api_view(["GET"])
def getPosts(request):
    posts = Post.objects.all()
    serialized_posts = PostSerializer(posts, many=True)
    return Response(serialized_posts.data)


@api_view(["GET"])
def getPost(request, pk):
    post = Post.objects.get(slug=pk)
    post = PostSerializer(post)
    return Response(post.data)
