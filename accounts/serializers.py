from rest_framework import serializers
from django.contrib.auth import get_user_model


class TimtecUserSerializer(serializers.ModelSerializer):
    name = serializers.Field(source='get_full_name')
    picture = serializers.Field(source='get_picture_url')
    is_profile_filled = serializers.BooleanField(source='is_profile_filled')

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'name', 'first_name', 'last_name',
                  'biography', 'picture', 'is_profile_filled')


class TimtecUserAdminSerializer(TimtecUserSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'name', 'email', 'is_active', 'is_superuser', 'first_name', 'last_name',)


class TimtecUserAdminCertificateSerializer(TimtecUserSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'name', 'email', 'username')


class StateSerializer(serializers.Serializer):
    code = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)


class CitySerializer(serializers.Serializer):
    state = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
