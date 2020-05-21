from django.core.management.base import BaseCommand
from facial_recognition.queue_processor import process_queue


class Command(BaseCommand):
    '''
    Management command to run the facial recognition queue checker on loop
    '''
    def handle(self, *args, **options):
        process_queue()