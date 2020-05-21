from django.core.management.base import BaseCommand
from family_tree.models import Family
from facial_recognition.train import process_family


class Command(BaseCommand):
    '''
    Management command to rebuild the facial recognition model
    Needs to be run if sklearn has any breaking model changes
    '''
    def handle(self, *args, **options):

        print('===Rebuilding Facial Models===')

        for family in Family.objects.all():

            print('')
            print('Building: {0}'.format(family.description))
            process_family(family.id)
