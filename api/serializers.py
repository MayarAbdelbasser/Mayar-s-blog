from rest_framework import serializers
from blog.models import Post, Author, Tag


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False)
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = "__all__"
