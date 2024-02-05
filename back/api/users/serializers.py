from rest_framework import serializers
from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["id", 'username', 'email', 'first_name', 'last_name', 'date_joined',
                  'is_active', 'is_staff', 'is_superuser', 'password', 'role']
