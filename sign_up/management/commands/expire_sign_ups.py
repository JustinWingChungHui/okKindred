from django.core.management.base import BaseCommand
from sign_up.models import SignUp

class Command(BaseCommand):
    args = ''
    help = 'Expires any old pending email confirmations'

    def handle(self, *args, **options):
        SignUp.objects.remove_expired_sign_ups()