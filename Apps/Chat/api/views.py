from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Subquery, OuterRef
from django.core.files.storage import default_storage
from rest_framework import exceptions
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateAPIView, UpdateAPIView, \
    RetrieveAPIView, RetrieveUpdateDestroyAPIView
from ..models import Members, Room, Messages
from .paginator import RoomsPaginator, MessagesPaginator, MembersPaginator
from .mixins import BaseChatAPI, RoomMixin, MemberMixin
from .serializers import (
    RoomsSerializer,
    RoomSettingsSerializer,
    JoinRoomSerializer,
    RoomCoverSerializer,
    RoomSerializer,
    MembersSerializer,
    MemberSerializer,
    MessagesSerializer
)


class RoomsAPI(BaseChatAPI, ListCreateAPIView):
    throttle_scope = 'rooms', '100/min'
    serializer_class = RoomsSerializer
    pagination_class = RoomsPaginator

    def get_queryset(self):
        return Room.objects.filter(id__in=Subquery(
            Members.objects\
                .filter(user=self.request.user, room=OuterRef('id'), is_pending=False, is_deleted=False) \
                .values_list('room')
        ), is_deleted=False).order_by('-id')

    def perform_create(self, serializer):
        with transaction.atomic():
            _room = serializer.save(
                creator=self.request.user,
                password=make_password(serializer.validated_data['password'])
            )
            Members(user=self.request.user, room=_room, is_admin=True, is_pending=False).save()


class JoinRoomAPI(BaseChatAPI, RetrieveUpdateAPIView):
    throttle_scope = 'join-room', '100/min'
    serializer_class = JoinRoomSerializer

    queryset = Room.objects.filter(is_closed=False, is_deleted=False).all()
    lookup_field = 'code'
    lookup_url_kwarg = 'Room_Code'

    def perform_update(self, serializer):
        if not check_password(serializer.validated_data['password'], serializer.instance.password):
            raise exceptions.PermissionDenied(detail='Wrong Password')
        
        if not Members.objects.filter(user=self.request.user, room=serializer.instance).exists():
            Members(
                user=self.request.user, room=serializer.instance,
                is_pending = True if serializer.instance.need_permission else False
            )


class RoomSettingsAPI(BaseChatAPI, RoomMixin, RetrieveUpdateAPIView):
    throttle_scope = 'room-settings', '100/min'
    serializer_class = RoomSettingsSerializer

    is_admin = True
    need_room_object = True
    
    def perform_update(self, serializer):
        if 'password' in serializer.validated_data:
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        serializer.save()


class RoomCoverSettingsAPI(BaseChatAPI, RoomMixin, UpdateAPIView):
    throttle_scope = 'room-cover-settings', '100/min'
    serializer_class = RoomCoverSerializer

    is_admin = True
    need_room_object = True
    
    def perform_update(self, serializer):
        if 'cover' in serializer.validated_data:
            if self.room.get_old_image_name() != serializer.validated_data['cover'] and (
                self.room.get_old_image_name() != 'rooms/defaultCover.jpg'
            ):
                default_storage.delete(self.room.get_old_image_path())
            serializer.save()


class RoomAPI(BaseChatAPI, RoomMixin, RetrieveAPIView):
    throttle_scope = 'room', '100/min'
    serializer_class = RoomSerializer
    need_room_object = True


class MembersAPI(BaseChatAPI, RoomMixin, ListAPIView):
    throttle_scope = 'members', '100/min'
    serializer_class = MembersSerializer
    pagination_class = MembersPaginator

    is_admin = True

    def get_queryset(self):
        return Members.objects.filter(is_deleted=False, room=self.room)


class MemberAPI(BaseChatAPI, MemberMixin, RoomMixin, RetrieveUpdateDestroyAPIView):
    throttle_scope = 'member', '100/min'
    serializer_class = MemberSerializer
    
    is_admin = True
    need_member_object = True
    
    def perform_update(self, serializer):
        serializer.save(
            is_admin=True if 'upgrade' in self.request.query_params else serializer.instance.is_admin,
            is_pending=serializer.instance.is_pending if 'upgrade' in self.request.query_params else False
        )

    def perform_destroy(self, instance: Members):
        if self.room.creator == self.request_member.user:
            raise exceptions.PermissionDenied(detail='Is Creator')
        
        elif self.request_member.is_admin and not self.is_creator():
            raise exceptions.PermissionDenied(detail='Is Admin')

        
        if 'degrade' in self.request.query_params:
            self.request_member.is_admin = False
        else:
            self.request_member.is_deleted = True
            
        self.request_member.save()


class MessagesAPI(BaseChatAPI, RoomMixin, ListAPIView):
    throttle_scope = 'messages', '100/min'
    serializer_class = MessagesSerializer
    pagination_class = MessagesPaginator

    def get_queryset(self):
        return Messages.objects.filter(is_deleted=False, room=self.room)
