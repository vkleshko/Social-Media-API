from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext as _

from social_media.models import Follow


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password")
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):
        """Create user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)


class UserTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""

        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"), email=email, password=password
        )

        if not user:
            msg = _("Unable to authenticate with provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user

        return attrs


class FollowerSerializer(serializers.ModelSerializer):
    follow_me_email = serializers.EmailField(source="follower.email")

    class Meta:
        model = Follow
        fields = ("id", "follow_me_email")


class FollowedSerializer(serializers.ModelSerializer):
    follow_him_email = serializers.EmailField(source="followed.email")

    class Meta:
        model = Follow
        fields = ("id", "follow_him_email")


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "profile_image", "bio")


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("profile_image", "bio")

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class ProfileDetailSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    follow_me_list = FollowerSerializer(read_only=True, many=True)
    follow_him_list = FollowedSerializer(read_only=True, many=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "is_staff",
            "profile_image",
            "bio",
            "followers_count",
            "follow_me_list",
            "follow_him_list",
        )

    def get_followers_count(self, obj):
        return obj.followed.count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["follow_me_list"] = FollowerSerializer(
            instance.followed.all(), many=True
        ).data
        data["follow_him_list"] = FollowedSerializer(
            instance.follower.all(), many=True
        ).data

        return data
