from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class TimtecUserSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='get_full_name')
    picture = serializers.ReadOnlyField(source='get_picture_url')
    is_profile_filled = serializers.BooleanField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'name', 'first_name', 'last_name',
                  'biography', 'picture', 'is_profile_filled')


class TimtecUserAdminSerializer(TimtecUserSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'name', 'email', 'is_active', 'is_superuser', 'first_name', 'last_name', 'picture', 'groups', )
        depth = 1


class TimtecUserAdminCertificateSerializer(TimtecUserSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'name', 'email', 'username')


class GroupAdminSerializer(serializers.ModelSerializer):

    users = TimtecUserSerializer(many=True, read_only=True, source="user_set")

    class Meta:
        model = Group
        fields = ('id', 'name', 'users', )
        depth = 1


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')
