from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _



class Feedback(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(_('Feedback Title'), max_length=100)
    feedback = models.CharField(_('Feedback'), max_length=1000)
    is_deleted = models.BooleanField(_('Is Feedback Deleted'), default=False)
    created_at = models.DateTimeField(_('Feedback Creation Date'), auto_now_add=True)
