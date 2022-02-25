from rest_framework import serializers
from ..models import Room, Members, Messages


class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name', 'password', 'description', 'cover', 'created_at', 'code']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['created_at', 'cover', 'code']


class JoinRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['code', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class RoomSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ['is_deleted']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['creator', 'code', 'last_updated', 'created_at', 'cover']


class RoomCoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['cover']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ['creator', 'password', 'is_closed', 'is_deleted', 'need_permission', 'last_updated']


class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        exclude = ['is_deleted']


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        exclude = ['is_deleted']
        read_only_fields = ['user', 'room', 'is_admin', 'is_pending', 'last_updated', 'created_at']


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        exclude = ['is_deleted']
