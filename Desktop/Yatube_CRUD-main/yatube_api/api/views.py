from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        serializer.save(author=self.request.user, post_id=post_id)

@api_view(['GET'])
def api_root(request, format=None):
    """
    Корневой эндпоинт API с ссылками на все доступные ресурсы
    """
    return Response({
        'api-token-auth': reverse('api_token_auth', request=request, format=format),
        'posts': reverse('posts-list', request=request, format=format),
        'groups': reverse('groups-list', request=request, format=format),
        'comments': 'http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/',
        'admin': 'http://127.0.0.1:8000/admin/',
    })