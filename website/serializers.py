from rest_framework import serializers
from .models import StudySessionMessage
from django.utils import timezone


class StudySessionMessageSerializer(serializers.ModelSerializer):
    """
    class responsible with the serialization of a message from the study session chat
    """
    sender = serializers.SerializerMethodField()
    datetime = serializers.SerializerMethodField()
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = StudySessionMessage
        fields = ['sender', 'message_content',
                  'datetime', 'profile_picture_url']

    def get_sender(self, obj):
        if obj is not None:
            return obj.user.username

        return None

    def get_datetime(self, obj):
        if obj is None:
            return None

        months = {
            1: "Jan",
            2: "Feb",
            3: "Mar",
            4: "Apr",
            5: "May",
            6: "Jun",
            7: "Jul",
            8: "Aug",
            9: "Sep",
            10: "Oct",
            11: "Nov",
            12: "Dec"
        }

        created_at = timezone.localtime(obj.create)
        datetime = f"{created_at.day}  {months[created_at.month]}  {created_at.hour}:{created_at.minute}"

        return datetime

    def get_profile_picture_url(self, obj):
        if not obj.user.user_profile.profile_picture:
            default_profile_picture = "https://robohash.org/default_profile_picture?set=set1&size=200x200"
            return default_profile_picture

        return obj.user.user_profile.profile_picture.url
