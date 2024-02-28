from django.urls import path

from user.views import (
    UserCreateView,
    CreateTokenView,
    ProfileUpdateView,
    ProfileListView,
    DeleteTokenView,
    ProfileDetailView,
)

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="create"),
    path("login/", CreateTokenView.as_view(), name="token"),
    path("logout/", DeleteTokenView.as_view(), name="token-delete"),
    path("profile/", ProfileDetailView.as_view(), name="detail"),
    path("profile/update/", ProfileUpdateView.as_view(), name="update"),
    path("profiles/", ProfileListView.as_view(), name="profiles-list"),

]

app_name = "user"
