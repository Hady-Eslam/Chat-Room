from django.core.files.storage import default_storage
from django.views.generic import FormView, UpdateView
from django.urls import reverse_lazy as reverse
from django.contrib.auth import logout
from django.utils import timezone
from Apps.Auth.mixins import SuccessMessageMixin, LoginRequiredMixin
from .mixins import ProfileMixin
from .forms import ProfileForm, PasswordForm, SettingsForm
import os



class ProfileView(LoginRequiredMixin, ProfileMixin, SuccessMessageMixin, UpdateView):
    success_flash_message_name = 'profile_success'
    success_flash_message = 'Your Profile has Been Changed Successfully'

    success_url = reverse('Profile:Profile')
    form_class = ProfileForm

    def get_object(self, queryset=None):
        self.profile.save_old_image_path()
        return self.profile
    
    def form_valid(self, form):
        self.profile.user.first_name = form.cleaned_data.pop('first_name')
        self.profile.user.last_name = form.cleaned_data.pop('last_name')
        self.profile.user.save()

        if self.profile.get_old_image_name() != form.cleaned_data['avatar'] and (
            self.profile.get_old_image_name() != 'user/User.png'
        ):
            default_storage.delete(self.profile.get_old_image_path())

        form.cleaned_data['updated_at'] = timezone.now()

        return super().form_valid(form)
    

class PasswordView(LoginRequiredMixin, ProfileMixin, FormView):
    success_url = reverse('Profile:Password')
    form_class = PasswordForm

    def form_valid(self, form):
        if self.request.user.check_password(form.cleaned_data['old_password']) and (
            self.request.user.get_username() != os.environ.get('GUEST_USERNAME')
        ):
            self.request.user.set_password(form.cleaned_data['password'])
            self.request.user.save()
            return super().form_valid(form)

        form.add_error('old_password', 'Invalid Old Password Or User Guest Does Not Have Permission To Change Password')
        return super().form_invalid(form)


class SettingsView(LoginRequiredMixin, ProfileMixin, FormView):
    success_url = reverse('Auth:Login')
    form_class = SettingsForm

    def form_valid(self, form):
        if form.cleaned_data['username'] == self.request.user.get_username() and (
            self.request.user.check_password(form.cleaned_data['password'])
        ):
            if not self.request.user.is_superuser and (
                self.request.user.get_username() != os.environ.get('GUEST_USERNAME')
            ):
                self.request.user.is_active = False
                self.request.user.save()
                logout(self.request)
                return super().form_valid(form)
            else:
                form.add_error('username', 'Can Not Deactivate Superuser And Guest Accounts')
        else:
            form.add_error('username', 'Invalid Username Or Wrong Password')
        return super().form_invalid(form)
