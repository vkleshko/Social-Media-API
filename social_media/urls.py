from django.urls import path, include
from rest_framework import routers

from social_media.views import (
    PostViewSet,
    CommentViewSet,
    LikeViewSet,
    FollowViewSet,
    OwnPostListView,
    FollowedPostListView,
    LikedPostListView,
)

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)
router.register("likes", LikeViewSet)
router.register("follows", FollowViewSet)

urlpatterns = [
    path("posts/my/", OwnPostListView.as_view(), name="own-posts"),
    path("posts/followed/", FollowedPostListView.as_view(), name="followed-posts"),
    path("posts/liked/", LikedPostListView.as_view(), name="followed-posts"),
    path("", include(router.urls)),

]

app_name = "social_media"
