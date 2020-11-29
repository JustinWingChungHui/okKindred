from django.conf import settings
import boto3
import os


def upload_file_to_s3(filename_and_path):
    '''
    Uploads a file to S3
    '''
    file = str(filename_and_path)
    if file:
        client = boto3.client('s3')
        client.upload_file(settings.MEDIA_ROOT + file, settings.AWS_STORAGE_BUCKET_NAME, file)


def remove_file_from_s3(filename_and_path):
    '''
    Removes file from S3
    '''
    file = str(filename_and_path)
    if file:

        try:
            client = boto3.client('s3')
            client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=str(file))
        except:
            pass


def get_file_from_s3(filename_and_path):
    '''
    Gets a file from S3
    '''
    file = str(filename_and_path)

    # Create directory if it does not exist
    directory, filename = os.path.split(settings.MEDIA_ROOT + file)

    if not os.path.exists(directory):
        os.makedirs(directory)

    client = boto3.client('s3')
    client.download_file(settings.AWS_STORAGE_BUCKET_NAME, file, settings.MEDIA_ROOT + file)

