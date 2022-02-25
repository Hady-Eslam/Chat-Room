from django.utils import timezone
from django.db import transaction
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework import exceptions
from rest_framework import status
from ..models import UserToken
from ..helper import Random, Email
from .mixins import BaseMixin
from .serializers import SignupSerializer, ForgetPasswordSerializer, ResetPasswordSerializer
import datetime, os



class SignupAPI(BaseMixin, CreateAPIView):
    throttle_scope = 'signup', '100/hour'
    serializer_class = SignupSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            _User = serializer.save(is_active=False,
                password=make_password(
                    serializer.validated_data['password'] if serializer.validated_data['password'] else ''
                )
            )
            _Token = UserToken(user=_User, token=Random.create_random_token(50, 70))
            _Token.save()
            Email.apiSendConfirm(self.request, _Token)


class ConfirmSignupAPI(BaseMixin, APIView):
    throttle_scope = 'confirm-signup', '100/hour'

    def post(self, request, *args, **kwargs):
        _Token = UserToken.objects.filter(token=self.request.query_params.get("Token"))\
            .filter(created_at__gte=timezone.now()-datetime.timedelta(days=2))\
                .filter(user__is_active=False).filter(user__last_login=None).first()
        
        if _Token is None: raise exceptions.NotFound(detail='Token Or User Not Found')

        with transaction.atomic():
            _Token.user.is_active = True
            _Token.created_at = timezone.now()-datetime.timedelta(days=3)
            _Token.user.save()
            _Token.save()

        return Response(status=status.HTTP_200_OK)


class ForgetPasswordAPI(BaseMixin, UpdateModelMixin, GenericAPIView):
    throttle_scope = 'forget-password', '100/hour'
    serializer_class = ForgetPasswordSerializer
    
    def get_object(self): pass

    def post(self, request, *args, **kwargs):
        return self.update(request, args, kwargs)
    
    def perform_update(self, serializer):
        _Token = UserToken.objects.filter(user__username=serializer.validated_data['username'])\
            .filter(user__is_active=True).exclude(user__username=os.environ.get('GUEST_USERNAME')).first()
        
        if _Token is None:
            raise exceptions.NotFound(detail='User Not Found Or is Not Active Or Guest User')
        
        _Token.token = Random.create_random_token(50, 70)
        _Token.created_at = timezone.now()
        _Token.save()

        Email.apiSendResetPassword(self.request, _Token)


class ResetPasswordAPI(BaseMixin, RetrieveUpdateAPIView):
    throttle_scope = 'reset-password', '100/hour'
    serializer_class = ResetPasswordSerializer

    def get_object(self):
        self.token = UserToken.objects.filter(token=self.request.query_params.get("Token"))\
            .filter(created_at__gte=timezone.now()-datetime.timedelta(minutes=30))\
                .filter(user__is_active=True).first()
        if self.token is None: raise exceptions.NotFound(detail='Token Or User Not Found')
        return self.token

    def perform_update(self, serializer):
        with transaction.atomic():
            self.token.user.set_password(serializer.validated_data["password"])
            self.token.created_at = timezone.now()-datetime.timedelta(days=3)
            self.token.user.save()
            self.token.save()
