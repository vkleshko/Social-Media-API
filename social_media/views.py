from django.db.models import Count
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from social_media.models import Post, Comment, Like, Follow
from social_media.permisssions import IsOwnerOrReadOnly
from social_media.serializers import (
    PostCreateSerializer,
    PostListSerializer,
    CommentListSerializer,
    CommentCreateSerializer,
    PostDetailSerializer,
    LikeSerializer,
    FollowCreateSerializer,
    FollowListSerializer,
)


class PostViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Post.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = self.queryset.annotate(
            comments_count=Count("comments"),
            likes_count=Count("post_likes")
        ).select_related("user").prefetch_related("comments")

        post_content = self.request.query_params.get("content", None)
        owner = self.request.query_params.get("owner", None)

        if post_content:
            queryset = queryset.filter(content__icontains=post_content)

        if owner:
            queryset = queryset.filter(user__email__icontains=owner)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer

        if self.action == "create":
            return PostCreateSerializer

        if self.action == "retrieve":
            return PostDetailSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "content",
                type=str,
                description="Filtering by content (ex. ?content=social_media)"
            ),
            OpenApiParameter(
                "owner",
                type=str,
                description="Filtering by owner (ex. ?owner=admin@admin.com)"
            )
        ]
    )
    def list(self, request):
        return super().list(request)


class OwnPostListView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Post.objects.filter(user=request.user).annotate(
            comments_count=Count("comments"),
            likes_count=Count("post_likes")
        ).select_related("user")
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk, user=request.user)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowedPostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        followed_user_ids = self.request.user.follower.values_list(
            "followed_id", flat=True
        )
        return self.queryset.filter(user__id__in=followed_user_ids).annotate(
            comments_count=Count("comments"),
            likes_count=Count("post_likes")
        ).select_related("user")


class LikedPostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        liked_post_id = Like.objects.values_list(
            "post_id", flat=True
        )
        return self.queryset.filter(id__in=liked_post_id).annotate(
            comments_count=Count("comments"),
            likes_count=Count("post_likes")
        ).select_related("user")


class CommentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Comment.objects.select_related("post", "user")
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return CommentListSerializer

        if self.action == "create":
            return CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Like.objects.select_related("post", "user")
    serializer_class = LikeSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FollowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Follow.objects.select_related("follower", "followed")
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(follower=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return FollowListSerializer

        if self.action == "create":
            return FollowCreateSerializer

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)
