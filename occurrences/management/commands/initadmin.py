from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = 'admin'
        email = ''
        password = 'a'
        print('Creating account for %s ' % username)
        admin = User.objects.create_superuser(email=email, username=username, password=password)
        admin.is_active = True
        admin.is_admin = True
        admin.save()
