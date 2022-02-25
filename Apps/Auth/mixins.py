from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy as reverse
from braces import views
import os


class NotGuestUser(UserPassesTestMixin):

    def test_func(self):
        return bool(self.request.user.get_username() != os.environ.get('GUEST_USERNAME'))


class AnonymousRequiredMixin(views.AnonymousRequiredMixin):
    authenticated_redirect_url = reverse('')


class LoginRequiredMixin(views.LoginRequiredMixin):
    login_url = reverse('Auth:Login')


class SuccessMessageMixin:
    """
    Add a success message on successful form submission.
    """
    success_flash_message_name = ''
    success_flash_message = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_flash_message:
            self.request.flash_message.set(self.success_flash_message_name, self.success_flash_message)
        return response
