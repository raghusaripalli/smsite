from rest_framework import serializers

from myapp.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('weather','date_time','quote', 'user_text', 'location', 'alarm', 'timezone')