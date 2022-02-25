from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from ...models import UserToken
from ...helper import Random
import os


class Command(BaseCommand):
    help = 'Create Guest User With User Token'

    def handle(self, *args, **options):
        with transaction.atomic():
            _User = User.objects.create_user(
                username=os.environ.get('GUEST_USERNAME'),
                email=os.environ.get('GUEST_EMAIL'),
                password=os.environ.get('GUEST_PASSWORD'),
                first_name=os.environ.get('GUEST_FIRSTNAME')
            )
            UserToken(user=_User, token=Random.create_random_token(50, 70)).save()

        self.stdout.write(self.style.SUCCESS('{ Guest } User Created Successfully'))
