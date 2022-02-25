from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework import exceptions
from ..models import Room, Members
from .versioning import Versioning
from .throttles import ChatThrottleClass


class BaseChatAPI:
    permission_classes = [IsAuthenticated]
    throttle_classes = [ChatThrottleClass]
    renderer_classes = [JSONRenderer]
    versioning_class = Versioning


class RoomMixin:

    is_admin = False
    need_room_object = False

    def initial(self, request, *args, **kwargs):
        super(RoomMixin, self).initial(request, *args, **kwargs)
        
        self.room = Room.objects.filter(code=kwargs['Room_Code'], is_deleted=False).first()
        if self.room is None:
            raise exceptions.NotFound(detail='Room Not Found')
        
        self.member = Members.objects.filter(user=request.user, room=self.room, is_deleted=False).first()
        if self.member is None:
            raise exceptions.PermissionDenied(detail='Not Member')
        elif self.member.is_pending:
            raise exceptions.PermissionDenied(detail='Still Pending')
        elif self.is_admin and not self.member.is_admin:
            raise exceptions.PermissionDenied(detail='User is Not Admin')

    def is_creator(self):
        return self.room.creator == self.member.user
    
    def get_object(self):
        self.room.save_old_image_path()
        return self.room if self.need_room_object else super(RoomMixin, self).get_object()



class MemberMixin:

    need_member_object = False

    def initial(self, request, *args, **kwargs):
        super(MemberMixin, self).initial(request, *args, **kwargs)

        self.request_member = Members.objects.filter(id=kwargs['Member_id'], is_deleted=False)\
            .filter(room=self.room).first()
            
        if self.request_member is None:
            raise exceptions.NotFound(detail='Member Not Found')
        
    def get_object(self):
        return self.request_member if self.need_member_object else super(MemberMixin, self).get_object()
