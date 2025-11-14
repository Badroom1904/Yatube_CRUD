from rest_framework import serializers
from posts.models import Post, Group, Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post',)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    comments = CommentSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Post
        fields = (
            'id', 'text', 'author', 'image',
            'group', 'pub_date', 'comments'
        )
