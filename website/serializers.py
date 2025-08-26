from rest_framework import serializers
from .models import StudySessionMessage


class StudySessionMessageSerializer(serializers.ModelSerializer):
    """
    class responsible with the serialization of a message from the study session chat
    """
    sender = serializers.SerializerMethodField()

    class Meta:
        model = StudySessionMessage
        fields = ['sender', 'message_content']

    def get_sender(self, obj):
        if obj is not None:
            return obj.user.username

        return None
