from django.apps import apps
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse_lazy as reverse
from django.views.generic import TemplateView, CreateView, View
from Apps.Auth.mixins import LoginRequiredMixin, SuccessMessageMixin
from Apps.Profile.mixins import ProfileMixin
from .models import Feedback
import os


class HomeView(ProfileMixin, TemplateView):
    pass

class FeedbackView(LoginRequiredMixin, ProfileMixin, SuccessMessageMixin, CreateView):
    success_flash_message_name = 'success_create_feedback'
    success_flash_message = 'Your Feedback Submitted Successfully'

    success_url = reverse('Info:Feedback')

    model = Feedback
    fields = ['title', 'feedback']

    def form_valid(self, form):
        if self.request.user.get_username() == os.environ.get('GUEST_USERNAME'):
            form.add_error('title', 'Guest User Can Not Make Feedback')
            return super().form_invalid(form)
        _Feedback = form.save(commit=False)
        _Feedback.user = self.request.user
        return super().form_valid(form)

class WhoIAmView(ProfileMixin, TemplateView):
    pass

class DownloadCV(View):

    def get(self, request):
        _File_Path = apps.get_app_config('Info').path + settings.MEDIA_URL + 'Django Backend Developer.pdf'

        with open(_File_Path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="Django Backend Developer.pdf"'
            return response
