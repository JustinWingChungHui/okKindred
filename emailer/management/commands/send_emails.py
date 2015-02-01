from django.core.management.base import BaseCommand
from emailer.models import Email

class Command(BaseCommand):
    args = ''
    help = 'Sends any update emails'

    def handle(self, *args, **options):
        Email.objects.create_and_send_emails()