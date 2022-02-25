from braces.views import LoginRequiredMixin, AnonymousRequiredMixin
from django.views.generic import TemplateView, RedirectView, FormView, CreateView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy as reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction
from .models import UserToken
from .helper import Random, Email
from .mixins import AnonymousRequiredMixin, SuccessMessageMixin
from .forms import LoginForm, ForgetPasswordForm, ResetPasswordForm
import datetime, os



class Signup(AnonymousRequiredMixin, SuccessMessageMixin, CreateView):

    success_flash_message_name = 'success_signup'
    success_flash_message = 'Please Check Your Email To Activate Account'

    success_url = reverse('Auth:Signup')

    model = User
    fields = ['username', 'email', 'password']

    def form_valid(self, form):
        with transaction.atomic():
            _User = form.save(commit=False)
            _User.set_password(_User.password if _User.password else '')
            _User.is_active = False
            _User.save()

            _Token = UserToken(user=_User, token=Random.create_random_token(50, 70))
            _Token.save()

            Email.sendConfirm(_Token, self.request.build_absolute_uri)
            return super().form_valid(form)



class ConfirmSignup(AnonymousRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        _Token = UserToken.objects.filter(token=self.request.GET.get('Token'))\
            .filter(user__is_active=False).filter(user__last_login=None)\
                .filter(created_at__gte=timezone.now()-datetime.timedelta(days=2)).first()

        if _Token is None:
            return super().get_context_data(Found=False, **kwargs)
        
        with transaction.atomic():
            _Token.user.is_active = True
            _Token.created_at = timezone.now()-datetime.timedelta(days=3)
            _Token.user.save()
            _Token.save()
            return super().get_context_data(Found=True, **kwargs)



class Login(FormView):
    
    form_class = LoginForm
    success_url = reverse('')

    def form_valid(self, form):
        _User = authenticate(
            self.request, username=form.cleaned_data['username'], password=form.cleaned_data['password']
        )

        if _User:
            logout(self.request) if self.request.user.is_authenticated else None
            login(self.request, _User)
            return super().form_valid(form)
        
        form.add_error('username', 'UserName Or Password is Incorrect Or User is InActive')
        return super().form_invalid(form)



class LoginAsGuest(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        _User = authenticate(
            self.request, username=os.environ.get('GUEST_USERNAME'), password=os.environ.get('GUEST_PASSWORD')
        )
        if _User:
            logout(self.request) if self.request.user.is_authenticated else None
            login(self.request, _User)
            return reverse('')
        return reverse('Auth:Login')



class Logout(LoginRequiredMixin, RedirectView):
    login_url = reverse('Auth:Login')
    
    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return reverse('Auth:Login')



class ForgetPassword(AnonymousRequiredMixin, SuccessMessageMixin, FormView):

    success_flash_message_name = 'success_forget_password'
    success_flash_message = 'Reset Password Link Has Been Sent To Your Email'

    form_class = ForgetPasswordForm
    success_url = reverse('Auth:Forget-Password')

    def form_valid(self, form):

        _Token = UserToken.objects.filter(user__username=form.cleaned_data['username'])\
            .filter(user__is_active=True).exclude(user__username=os.environ.get('GUEST_USERNAME')).first()
        
        if _Token is None:
            form.add_error('username', 'User Not Found Or is Not Active Or Guest User')
            return super().form_invalid(form)
        
        _Token.token = Random.create_random_token(50, 70)
        _Token.created_at = timezone.now()
        _Token.save()

        Email.SendResetPassword(_Token, self.request.build_absolute_uri)
        return super().form_valid(form)



class ResetPassword(AnonymousRequiredMixin, SuccessMessageMixin, FormView):

    success_flash_message_name = 'success_reset_password'
    success_flash_message = 'Your Password Has Been Changed Successfuly'

    form_class = ResetPasswordForm
    success_url = reverse('Auth:Login')

    def get_context_data(self, **kwargs):
        _Token = UserToken.objects.filter(token=self.request.GET.get('Token'), user__is_active=True)\
            .filter(created_at__gte=timezone.now()-datetime.timedelta(minutes=30)).first()
        return super().get_context_data(token=_Token, **kwargs)

    def form_valid(self, form):
        _Token = UserToken.objects.filter(token=self.request.GET.get('Token'), user__is_active=True)\
            .filter(created_at__gte=timezone.now()-datetime.timedelta(minutes=30)).first()

        if not _Token:
            form.add_error('password', 'Token Not Found')
            return super().form_invalid(form)
        
        with transaction.atomic():
            _Token.user.set_password(form.cleaned_data['password'])
            _Token.created_at = timezone.now()-datetime.timedelta(days=3)
            _Token.user.save()
            _Token.save()
            return super().form_valid(form)
