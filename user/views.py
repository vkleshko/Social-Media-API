from django.contrib.auth import get_user_model, logout
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from user.serializers import (
    UserSerializer,
    UserTokenSerializer,
    ProfileUpdateSerializer,
    ProfileListSerializer,
    ProfileDetailSerializer
)


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = UserTokenSerializer


class DeleteTokenView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)


class ProfileListView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ProfileListSerializer

    def get_queryset(self):
        queryset = self.queryset

        email = self.request.query_params.get("email", None)
        if email:
            queryset = queryset.filter(email__icontains=email)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "email",
                type=str,
                description="Filtering by email (ex. ?email=admin@admin.com)"
            )

        ]
    )
    def list(self, request):
        return super().list(request)


class ProfileDetailView(generics.RetrieveAPIView):
    serializer_class = ProfileDetailSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
