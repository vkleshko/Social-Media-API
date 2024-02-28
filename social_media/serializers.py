from rest_framework import serializers

from social_media.models import Comment, Post, Like, Follow


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "post", "content", "created_at")


class CommentListSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "user_email", "content", "created_at")


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "content", "created_at")


class PostListSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "user_email",
            "content",
            "created_at",
            "comments_count",
            "likes_count",
        )


class PostDetailSerializer(PostListSerializer):
    comments = CommentListSerializer(many=True, read_only=True)

    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ("comments",)


class LikeSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Like
        fields = ("id", "post", "user_email", "created_at")


class FollowCreateSerializer(serializers.ModelSerializer):
    follower = serializers.EmailField(read_only=True)

    class Meta:
        model = Follow
        fields = ("id", "follower", "followed", "created_at")


class FollowListSerializer(FollowCreateSerializer):
    followed = serializers.EmailField()
