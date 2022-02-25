from braces import views
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, View
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import default_storage
from django.urls import reverse_lazy as reverse
from django.db.models import Subquery, OuterRef
from django.db import transaction
from django.utils import timezone
from Apps.Profile.mixins import ProfileMixin
from Apps.Auth.mixins import SuccessMessageMixin
from .mixins import RoomMixin, LoginRequiredMixin, MemberMixin
from .models import Room, Members, Messages
from .forms import JoinRoomForm



class HomeView(LoginRequiredMixin, ProfileMixin, ListView):

    def get_queryset(self):
        return Room.objects.filter(id__in=Subquery(
            Members.objects.\
                filter(user=self.request.user, room=OuterRef('id'), is_pending=False, is_deleted=False) \
                .values_list('room')
        ), is_deleted=False).order_by('-id')


class CreateRoomView(LoginRequiredMixin, ProfileMixin, SuccessMessageMixin, CreateView):
    success_flash_message_name = 'create_room'
    success_flash_message = 'Your Room Created Successfully'

    success_url = reverse('Chat:Home')
    
    model = Room
    fields = ['name', 'password', 'description', 'cover']

    def form_valid(self, form):
        room = form.save(commit=False)
        room.creator = self.request.user
        room.password = make_password(room.password if room.password else '')
        with transaction.atomic():
            room.save()
            Members(user=self.request.user, room=room, is_admin=True, is_pending=False).save()
        return super().form_valid(form)


class RoomView(LoginRequiredMixin, ProfileMixin, RoomMixin, TemplateView):

    def get_context_data(self, **kwargs):
        members = Members.objects.filter(room=self.room, is_deleted=False, is_pending=False)\
            .prefetch_related('user__profile')
        room_messages = Messages.objects.filter(room=self.room, is_deleted=False)\
            .prefetch_related('user__profile')
        return super().get_context_data(room_messages=room_messages, members=members, **kwargs)


class JoinRoomView(LoginRequiredMixin, views.JSONResponseMixin, View):

    def get(self, request, *args, **kwargs):
        _Exists = Room.objects.filter(code=request.GET.get('code'), is_deleted=False)\
            .filter(is_closed=False).exists()
        return self.render_json_response({}, status=200 if _Exists else 404)
    
    def post(self, request, *args, **kwargs):
        _Form = JoinRoomForm(request.POST)
        if not _Form.is_valid():
            return self.render_json_response(_Form.errors, status=400)

        _Room = Room.objects.filter(code=request.GET.get('code'), is_deleted=False)\
            .filter(is_closed=False).first()
            
        if _Room is None:
            return self.render_json_response({}, status=404)
        
        elif not check_password(_Form.cleaned_data['password'], _Room.password):
            return self.render_json_response({}, status=403)

        elif Members.objects.filter(user=request.user, room=_Room).exists():
            return self.render_json_response({}, status=200)
        
        Members(user=request.user, room=_Room, is_pending=True if _Room.need_permission else False).save()
        return self.render_json_response({}, status=201)


class SettingsView(LoginRequiredMixin, ProfileMixin, RoomMixin, SuccessMessageMixin, UpdateView):

    success_flash_message_name = 'update_room'
    success_flash_message = 'Your Room Updated Successfully'

    is_admin = True

    model = Room
    fields = ['name', 'description', 'is_closed', 'need_permission', 'password', 'cover']

    def get_success_url(self):
        return reverse('Chat:Settings', kwargs={'Room_Code': self.room.code})

    def get_object(self, *args, **kwargs):
        self.room.save_old_image_path()
        return self.room
    
    def form_valid(self, form):
        _Room = form.save(commit=False)
        if _Room.get_old_image_name() != form.cleaned_data['cover'] and (
            _Room.get_old_image_name() != 'rooms/defaultCover.jpg'
        ):
            default_storage.delete(_Room.get_old_image_path())

        _Room.password = make_password(form.cleaned_data['password'])
        _Room.last_updated = timezone.now()
        _Room.save()
        return super().form_valid(form)


class MembersView(LoginRequiredMixin, ProfileMixin, RoomMixin, ListView):

    is_admin = True

    def get_queryset(self):
        return Members.objects.filter(room=self.room, is_deleted=False).select_related('user')\
            .prefetch_related('user__profile')


class MemberView(LoginRequiredMixin, ProfileMixin, RoomMixin, MemberMixin, views.JSONResponseMixin, View):

    is_admin = True

    def patch(self, request, Room_Code, Member_id):
        if 'upgrade' in request.GET:
            self.Request_Member.is_admin = True
        else:
            self.Request_Member.is_pending = False
        self.Request_Member.save()
        return self.render_json_response({})


    def delete(self, request, Room_Code, Member_id):
        if self.room.creator == self.Request_Member.user:
            return self.render_json_response({'error': 'Is Creator'}, 403)
        
        elif self.Request_Member.is_admin and not self.is_creator():
            return self.render_json_response({'error': 'Is Admin'}, 403)
        
        if 'degrade' in request.GET:
            self.Request_Member.is_admin = False
        else:
            self.Request_Member.is_deleted = True
            
        self.Request_Member.save()
        return self.render_json_response({}, 204)
