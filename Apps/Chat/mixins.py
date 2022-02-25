from braces import views
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy as reverse
from django.http import Http404
from .models import Room, Members


class LoginRequiredMixin(views.LoginRequiredMixin):
    login_url = reverse('Auth:Login')


class RoomMixin:

    room = None
    member = None
    is_admin = False

    def dispatch(self, request, *args, **kwargs):

        self.room = Room.objects.filter(code=kwargs['Room_Code'], is_deleted=False).first()
        if self.room is None:
            raise Http404
        
        self.member = Members.objects.filter(user=request.user, room=self.room, is_deleted=False).first()
        if self.member is None:
            raise PermissionDenied('User is Not Room Member')
        elif self.member.is_pending:
            raise PermissionDenied('User Request is Still Pending')
        elif self.is_admin and not self.member.is_admin:
            raise PermissionDenied('User is Not Admin')

        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        return super().get_context_data(room=self.room, member=self.member, **kwargs)
    

    def is_creator(self):
        return self.room.creator == self.member.user



class MemberMixin:

    def dispatch(self, request, *args, **kwargs):
        self.Request_Member = Members.objects.filter(pk=kwargs['Member_id'])\
            .filter(room__code=kwargs['Room_Code']).first()
        if self.Request_Member is None: raise Http404
        return super().dispatch(request, *args, **kwargs)
