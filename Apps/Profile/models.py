from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from .storages import default_storage



def user_directory_path(instance, filename):
    return 'user/{0}'.format(filename)


class Profile(models.Model):

    class Gender(models.TextChoices):
        MALE = 'M', _('Male Gender')
        FEMALE = 'F', _('Female Gender')
        Unknown = 'U', _('Unknown Gender')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(_('Profile Picture'), storage=default_storage(),\
        upload_to=user_directory_path, default='user/User.png')
    bio = models.CharField(_('Bio'), max_length=100, null=True, blank=True)
    birthday = models.DateField(_('Birthday Date'), null=True, blank=True)
    gender = models.CharField(_('Gender'), max_length=2, choices=Gender.choices, default=Gender.Unknown)
    phone = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=30, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save_old_image_path(self):
        self.__File_Name = self.avatar.name
        self.__File_Path = self.avatar.path if self.avatar.name else ''
    
    def get_old_image_path(self):
        return self.__File_Path
    
    def get_old_image_name(self):
        return self.__File_Name
