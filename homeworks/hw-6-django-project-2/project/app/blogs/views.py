from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAuthorOrReadOnly, IsSelfOrReadOnly

from django.contrib.auth.models import User
from .models import Post, Comment
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSelfOrReadOnly]

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        user = self.get_object()
        user_stats = {
            "username": user.username,
            "total_posts": user.posts.count(),
            "total_comments": user.user_comments.count()
        }

        return Response(user_stats)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        low_weight_posts = Post.objects.annotate(
            likes_count=Count('likes')
        ).values('id', 'title', 'likes_count')

        return Response(low_weight_posts)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
