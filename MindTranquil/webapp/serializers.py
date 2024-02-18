from rest_framework import serializers
from .models import User, UserStats, Sessions


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    This serializer is used to convert User model instances to JSON objects and vice versa.
    """

    class Meta:
        model = User
        fields = "__all__"


class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStats
        fields = "__all__"


class SessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessions
        fields = "__all__"
