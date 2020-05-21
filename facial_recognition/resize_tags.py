from gallery.models import Image, Tag
from django.conf import settings
from facial_recognition.file_downloader import download_file, get_file_name, clear_directory
import face_recognition


def resize_tags(messages):
    '''
    Routine for resizing tags to match a recognized face
    '''

    try:
        clear_directory(settings.FACE_RECOG_RESIZE_TAG_TEMP_DIR)

        db_images = dict()
        face_locations_by_image_id = dict()

        tag_ids = []
        for message in messages:
            if message.integer_data:
                tag_ids.append(message.integer_data)

        tags = Tag.objects.filter(id__in=tag_ids).all()


        match_tags = 0

        for tag in tags:

            tag_center = {
                'x': (tag.x2 + tag.x1) / 2,
                'y': (tag.y2 + tag.y1) / 2,
            }


            if tag.image_id in db_images:
                # Using cached image if already downloaded
                db_image = db_images[tag.image_id]
                local_file = get_file_name(settings.FACE_RECOG_TAG_TEMP_DIR, db_image.large_thumbnail)


                locations = face_locations_by_image_id[tag.image_id]

            else:
                #Get image
                db_image = Image.objects.get(id=tag.image_id)
                db_images[tag.image_id] = db_image

                #Download file
                local_file = download_file(settings.FACE_RECOG_RESIZE_TAG_TEMP_DIR, db_image.large_thumbnail)


                #Loading the file into a numpy array
                image = face_recognition.load_image_file(local_file)

                # Faces found in image
                locations = face_recognition.face_locations(image)
                face_locations_by_image_id[tag.image_id] = locations


            for location in locations:
                top, right, bottom, left = location


                x1 = left / db_image.large_thumbnail_width
                x2 = right / db_image.large_thumbnail_width
                y1 = top / db_image.large_thumbnail_height
                y2 = bottom / db_image.large_thumbnail_height

                # Make sure centre of original tag is in detected face
                if x1 < tag_center['x'] and tag_center['x'] < x2:
                    if y1 < tag_center['y'] and tag_center['y'] < y2:
                        match_tags += 1

                        # Update tag with facial detection
                        tag.x1 = x1
                        tag.x2 = x2
                        tag.y1 = y1
                        tag.y2 = y2
                        tag.face_detected = True
                        tag.save()


        # Messages processed
        for message in messages:
            message.processed = True
            message.save()

    except Exception as e:
        print(e)
        for message in messages:
            message.error = True
            message.error_message = str(e)[:512]
            message.save()


    clear_directory(settings.FACE_RECOG_RESIZE_TAG_TEMP_DIR)


