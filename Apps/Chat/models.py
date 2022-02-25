from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from .helper import Random
from .storages import default_storage



def user_directory_path(instance, filename):
    return 'rooms/{0}'.format(filename)

def random_code(): return Random.create_random_token(10, 50)



class Room(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(_('Room Name'), max_length=100)
    code = models.CharField(_('Room Code'), max_length=100, unique=True, default=random_code)
    password = models.CharField(_('Room Password'), max_length=100)
    description = models.CharField(_('Room Description'), max_length=1000, null=True, default='')
    
    is_closed = models.BooleanField(_('Is Room Closed'), default=False)
    is_deleted = models.BooleanField(_('Is Room Deleted'), default=False)
    need_permission = models.BooleanField(_('Need Creator Permission To Enter'), default=True)
    cover = models.ImageField(_('Room Cover Image'), storage=default_storage,
        upload_to=user_directory_path, default='rooms/defaultCover.jpg')

    last_updated = models.DateTimeField(_('Room Last Updated Settings'), auto_now=True)
    created_at = models.DateTimeField(_('Room Creation Date'), auto_now_add=True)

    def save_old_image_path(self):
        self.__File_Name = self.cover.name
        self.__File_Path = self.cover.path if self.cover.name else ''
    
    def get_old_image_path(self):
        return self.__File_Path
    
    def get_old_image_name(self):
        return self.__File_Name


class Members(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    is_admin = models.BooleanField(_('Is Room Admin'), default=False)
    is_pending = models.BooleanField(_('Is Pending User'), default=True)
    is_deleted = models.BooleanField(_('Is User Deleted'), default=False)

    last_updated = models.DateTimeField(_('Member Last Updated Settings'), auto_now=True)
    created_at = models.DateTimeField(_('Member Creation Date'), auto_now_add=True)


class Messages(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Message_From_User')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='Message_Room')

    message = models.CharField(_('Room Message'), max_length=1000, default='')
    is_deleted = models.BooleanField(_('Is User Deleted'), default=False)

    created_at = models.DateTimeField(_('Message Creation Date'), auto_now_add=True)
