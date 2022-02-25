from django.core.files.storage import default_storage
from rest_framework.generics import RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework import exceptions
from .mixins import BaseProfileAPI, ProfileAPIMixin
from .serializers import ProfileSerializer, ProfileAvatarSerializer, PasswordSerializer
import os



class ProfileAPI(BaseProfileAPI, ProfileAPIMixin, RetrieveUpdateDestroyAPIView):
    throttle_scope = 'profile', '100/sec'
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.profile
    
    def perform_destroy(self, instance):
        if self.request.user.get_username() in [os.environ.get('GUEST_USERNAME'), os.environ.get('SUPER_USER_USERNAME')]:
            raise exceptions.PermissionDenied(detail={'Guest User And SuperUser Can Not Be Deactivated'})
        self.request.user.is_active = False
        self.request.user.save()


class ProfileAvatartAPI(BaseProfileAPI, ProfileAPIMixin, UpdateAPIView):
    throttle_scope = 'avatar', '10/hour'
    serializer_class = ProfileAvatarSerializer

    def get_object(self):
        self.profile.save_old_image_path()
        return self.profile
    
    def perform_update(self, serializer):
        default_storage.delete(self.profile.get_old_image_path() if serializer.validated_data['avatar'] else '')
        serializer.save()


class PasswordAPI(BaseProfileAPI, ProfileAPIMixin, UpdateAPIView):
    throttle_scope = 'password', '100/sec'
    serializer_class = PasswordSerializer

    def get_object(self):
        return self.request.user
    
    def perform_update(self, serializer):
        if self.request.user.get_username() == os.environ.get('GUEST_USERNAME'):
            raise exceptions.PermissionDenied(detail={'Guest User Can Not Change Password'})
        self.request.user.set_password(serializer.validated_data['password'])
        self.request.user.save()
