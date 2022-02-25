from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from ...models import UserToken
from ...helper import Random
import os


class Command(BaseCommand):
    help = 'Create Super User With User Token'

    def handle(self, *args, **options):
        with transaction.atomic():
            _User = User.objects.create_superuser(
                username=os.environ.get('SUPER_USER_USERNAME'),
                email=os.environ.get('SUPER_USER_EMAIL'),
                password=os.environ.get('SUPER_USER_PASSWORD'),
                first_name=os.environ.get('SUPER_USER_NAME'),
            )
            UserToken(user=_User, token=Random.create_random_token(50, 70)).save()
            
        self.stdout.write(self.style.SUCCESS('{ admin } User Created Successfully'))
