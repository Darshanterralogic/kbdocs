from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['password']
        read_only_fields = ['is_staff', 'is_superuser', 'created_by', 'updated_by']
