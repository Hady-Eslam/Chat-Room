from rest_framework.generics import CreateAPIView
from rest_framework import exceptions
from .serializers import FeedbackSerializer
from .mixins import BaseMixin
import os


class FeedbackAPI(BaseMixin, CreateAPIView):
    throttle_scope = 'feedback', '100/hour'
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        if self.request.user.get_username() == os.environ.get('GUEST_USERNAME'):
            raise exceptions.PermissionDenied(detail='Guest User Can not create feedback')
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)
