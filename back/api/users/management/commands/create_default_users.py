from users.models import User
from rest_framework.authtoken.models import Token
from django.core.management.base import BaseCommand

import os


class Command(BaseCommand):
    help = 'Create default superuser and user'

    def handle(self, *args, **options):
        try:
            print("Creating superuser...", end=" ", flush=True)
            username = os.environ.get("API_ADMIN_USER")
            psw = os.environ.get("API_ADMIN_PASSWORD")
            User.objects.create_superuser(username, 'admin@plintek.com', psw)
            print("OK", flush=True)
        except Exception as ex:
            print(f"ERROR - {ex}", flush=True)
