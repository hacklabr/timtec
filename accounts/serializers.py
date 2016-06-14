from rest_framework import serializers
from django.contrib.auth import get_user_model


class TimtecUserSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='get_full_name')
    picture = serializers.ReadOnlyField(source='get_picture_url')
    is_profile_filled = serializers.BooleanField()

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
