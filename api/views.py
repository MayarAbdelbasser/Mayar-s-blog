from .serializers import PostSerializer, AuthorSerializer, TagSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from blog.models import Post, Author
from rest_framework_simplejwt.tokens import RefreshToken


# specify request method
@api_view(["GET"])
def getRoutes(request):
    routes = [{"GET": "/api/"}, {"GET": "/api/posts/slug"}, {"POST": "/api/posts"}]
    return Response(routes)


@api_view(["GET", "POST"])
def getPosts(request):
    posts = Post.objects.all()
    serialized_posts = PostSerializer(posts, many=True)
    return Response(serialized_posts.data)


@api_view(["GET"])
def getPost(request, pk):
    post = Post.objects.get(slug=pk)
    post = PostSerializer(post)
    return Response(post.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createPost(request):
    serialized_posts = PostSerializer(
        data=request.data,
    )

    if serialized_posts.is_valid():
        serialized_posts.save()
        return Response(
            {"message": "Post created successfully", "data": serialized_posts.data},
            status=status.HTTP_201_CREATED,
        )

    return Response(serialized_posts.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deletePost(request):
    try:
        post = Post.objects.get(slug=request.data["post_slug"])

    except Post.DoesNotExist:
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    post.delete()
    return Response(
        {"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    email = request.data.get("email")
    password = request.data.get("password")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")

    if not email or not password or not first_name or not last_name:
        return Response(
            {"error": "email, first name, last name and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if Author.objects.filter(email=email).exists():
        return Response(
            {"error": "email is already exists."}, status=status.HTTP_400_BAD_REQUEST
        )
    author = Author.objects.create(
        email=email, password=password, first_name=first_name, last_name=last_name
    )
    return Response(
        {"message": "User created successfully"}, status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if not email or not password:
        return Response(
            {"error": "email and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        author = Author.objects.get(email=email, password=password)
    except Author.DoesNotExist:
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )

    refresh = RefreshToken.for_user(author)
    access_token = str(refresh.access_token)
    return Response(
        {"access": access_token, "refresh": str(refresh)}, status=status.HTTP_200_OK
    )
