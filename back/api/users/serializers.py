from rest_framework import serializers
from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["id", 'username', 'email', 'first_name', 'last_name', 'description',  'profile_picture', 'capture_count', 'following_count', "followers_count",  'level', 'private', 'date_joined',
                  'is_active', 'is_superuser', 'password', 'role']


class UserDetailedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["id", 'username', 'email', 'first_name', 'last_name', 'description', 'profile_picture', 'capture_count', 'following_count', "followers_count", 'followers', 'following', 'level', 'private', 'date_joined',
                  'is_active', 'is_superuser', 'password', 'role']
