from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _



class UserToken(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(_('Token'), max_length=100, default='')
    created_at = models.DateTimeField(_('Token Creation Date'), auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['token'], name='token_idx')
        ]
