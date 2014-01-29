from .models import TimtecUser
from rest_framework import serializers


class TimtecUserSerializer(serializers.ModelSerializer):
    name = serializers.Field(source='get_full_name')
    picture = serializers.Field(source='get_picture_url')

    class Meta:
        model = TimtecUser
        fields = ('id', 'username', 'name', 'first_name', 'last_name', 'biography', 'picture',)
