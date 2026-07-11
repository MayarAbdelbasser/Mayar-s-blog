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
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source="author"
    )
    author = AuthorSerializer(many=False, read_only=True)
    tags_id = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), source="tags", many=True, write_only=True
    )
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
