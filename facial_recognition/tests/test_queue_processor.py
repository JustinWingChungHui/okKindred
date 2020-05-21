from django.test import TestCase
from django.test.utils import override_settings
from facial_recognition.queue_processor import process_queue

@override_settings(SSLIFY_DISABLE=True, FACE_RECOG_MESSAGE_CHECK_INTERVAL_SECONDS=0)
class QueueProcessorTestCase(TestCase): # pragma: no cover


    def test_process_queue_runs_without_error(self):
        keep_running = False
        process_queue(keep_running)
