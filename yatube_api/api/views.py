from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from posts.models import Group, Post
from .serializers import CommentSerializer, GroupSerializer, PostSerializer
from .permissions import IsAuthorOrReadOnly


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsAuthorOrReadOnly
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticated,
        IsAuthorOrReadOnly
    )

    def perform_create(self, serializer):
        post = get_object_or_404(
            Post,
            pk=self.kwargs.get('post_id')
        )
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post = get_object_or_404(
            Post,
            pk=self.kwargs.get('post_id')
        )
        return post.comments
