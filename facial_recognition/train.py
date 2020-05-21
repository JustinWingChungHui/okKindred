# https://github.com/ageitgey/face_recognition/blob/master/examples/face_recognition_knn.py
from PIL import Image as PilImage
from family_tree.models import Person
from gallery.models import Tag
from facial_recognition.models import FaceModel
from django.conf import settings
from facial_recognition.file_downloader import download_file, clear_directory
import face_recognition
import os


def process_family(family_id):
    '''
    Creates a K Nearest neighbour model for a family
    using tagged photos and profile picture
    '''

    #Clearing working directory
    clear_directory(settings.FACE_RECOG_TRAIN_FACE_RECOGNITION_TEMP_DIR)

    face_model = FaceModel(family_id=family_id)

    people = Person.objects.filter(family_id=family_id)


    X = []
    y = []


    # Gets X and y data for each person
    for person in people:
        process_person(person, X, y)

    if (len(X) > 0):
        face_model.update_knn_classifier(X, y)

    else:
        print('Not enough data to create model')


def process_person(person, X, y):
    '''
    Processes images for one person
    '''
    # Creates directory for processing
    dir_name = os.path.join(settings.FACE_RECOG_TRAIN_FACE_RECOGNITION_TEMP_DIR, str(person.id))
    os.mkdir(dir_name)

    files = []

    # Gets their profile photo
    if person.large_thumbnail:
        files.append(download_file(dir_name, person.large_thumbnail))

    # Get all face detected tags for person
    tags = Tag.objects.select_related('image'
            ).filter(person_id= person.id
            ).filter(face_detected=True)


    for tag in tags:
        files.append(get_file_for_tag(tag, tag.image, dir_name))

    # Process Images
    for file in files:
        process_file(file, X, y, person.id)


def process_file(file, X, y, person_id):
    # Creating face encoding
    im = face_recognition.load_image_file(file)
    face_bounding_boxes = face_recognition.face_locations(im)

    # Add face encoding for current image to the training set
    if len(face_bounding_boxes) == 1:
        X.append(face_recognition.face_encodings(im, known_face_locations=face_bounding_boxes)[0])
        y.append(person_id)
    else:
        # No face found
        pass



def get_file_for_tag(tag, image, dir_name):
    '''
    Gets file for tag and image
    '''

    # Get image
    file = download_file(dir_name, image.large_thumbnail)
    original = PilImage.open(file)

    # Cropping image
    left = tag.x1 * image.large_thumbnail_width
    right = tag.x2 * image.large_thumbnail_width
    top = tag.y1 * image.large_thumbnail_height
    bottom = tag.y2 * image.large_thumbnail_height

    cropped = original.crop((left, top, right, bottom))
    cropped.save(file)

    return file







