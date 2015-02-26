from django.core.management.base import BaseCommand
from email_confirmation.models import EmailConfirmation

class Command(BaseCommand):
    args = ''
    help = 'Expires any old pending email confirmations'

    def handle(self, *args, **options):
        EmailConfirmation.objects.remove_expired_email_confirmations()