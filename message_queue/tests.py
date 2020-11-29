from django.utils import timezone
import datetime

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings

from message_queue.models import Queue, Message, create_message

@override_settings(SECURE_SSL_REDIRECT=False, 
                    MEDIA_ROOT=settings.MEDIA_ROOT_TEST,
                    MEDIA_URL=settings.MEDIA_URL_TEST,
                    AWS_STORAGE_BUCKET_NAME=settings.AWS_STORAGE_BUCKET_NAME_TEST)
class MessageQueueTestCase(TestCase): # pragma: no cover
    '''
    Tests for the Message Queue objects
    '''

    def test_create_resize_tag_message(self):
        '''
        Tests that we can create a queue
        '''
        queue = Queue.objects.get(name="resize_tag")

        message = Message(queue = queue,
                            string_data = "string_data",
                            integer_data = 12345,
                            float_data = 12.3456,
                            date_data = datetime.datetime.now(tz=timezone.utc))

        message.save()

        self.assertTrue(message.id > 0)



    def test_create_message(self):

        dt = datetime.datetime.now(tz=timezone.utc)

        message = create_message("resize_tag", 'string', dt, 1, 1.12354874)

        self.assertTrue(message.id > 0)
        self.assertFalse(message.processed)
        self.assertEqual('string', message.string_data)
        self.assertEqual(dt, message.date_data)
        self.assertEqual(1, message.integer_data)
        self.assertEqual(1.12354874, message.float_data)