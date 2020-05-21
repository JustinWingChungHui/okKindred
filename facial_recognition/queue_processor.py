from django.conf import settings
from message_queue.models import Queue, Message
from facial_recognition.resize_tags import resize_tags
from facial_recognition.image_face_detect import image_face_detect
from facial_recognition.profile_photo_process import profile_photo_process
from facial_recognition.tag_converted_process import tag_converted_process
from facial_recognition.person_deleted_update_face_model import person_deleted_update_face_model

import datetime
import time

def process_queue(keep_running = True):
    '''
    Processes all the facial recognition routines from the queue
    '''
    print('Getting queue data')

    resize_tag_queue_id = Queue.objects.get(name='resize_tag').id
    image_face_detect_id = Queue.objects.get(name='image_face_detect').id
    profile_photo_process_id = Queue.objects.get(name='profile_photo_process').id
    tag_converted_process_id = Queue.objects.get(name='tag_converted_process').id
    person_deleted_update_face_model_id = Queue.objects.get(name='person_deleted_update_face_model').id

    run_loop = True
    while run_loop:
        # Get unprocessed messages
        print('{} Checking queue...'.format(datetime.datetime.now()))

        # Get messages
        messages = (Message.objects
                    .filter(processed=False, error=False)
                    .order_by('creation_date')[:settings.FACE_RECOG_BATCH_SIZE])

        # Split up messages to be handled NB filter does weird stuff with object references
        resize_messages = []
        image_face_detect_messages = []
        profile_photo_process_messages = []
        tag_converted_process_messages = []
        person_deleted_update_face_model_messages = []

        for message in messages:
            if message.queue_id == resize_tag_queue_id:
                resize_messages.append(message)

            elif message.queue_id == image_face_detect_id:
                image_face_detect_messages.append(message)

            elif message.queue_id == profile_photo_process_id:
                profile_photo_process_messages.append(message)

            elif message.queue_id == tag_converted_process_id:
                tag_converted_process_messages.append(message)

            elif message.queue_id == person_deleted_update_face_model_id:
                person_deleted_update_face_model_messages.append(message)


        # Resize any image tags around detected faces
        if len(resize_messages) > 0:
            resize_tags(resize_messages)

        # Detects faces in any new gallery images
        if len(image_face_detect_messages) > 0:
            image_face_detect(image_face_detect_messages)

        # Updates face models if any new profile photos are uploaded
        if len(profile_photo_process_messages) > 0:
            profile_photo_process(profile_photo_process_messages)

        # Any suggested tags converted to actual tags
        if len(tag_converted_process_messages) > 0:
            tag_converted_process(tag_converted_process_messages)

        # Person deleted messages
        if len(person_deleted_update_face_model_messages) > 0:
            person_deleted_update_face_model(person_deleted_update_face_model_messages)

        print('==== Finished Processing Messages ====')

        # Wait 5 seconds until next queue check
        time.sleep(settings.FACE_RECOG_MESSAGE_CHECK_INTERVAL_SECONDS)

        if not keep_running:
            run_loop = False
