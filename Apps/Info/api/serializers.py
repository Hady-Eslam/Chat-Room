from rest_framework import serializers
from ..models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        exclude = ['is_deleted']
        read_only_fields = ['user', 'created_at']
