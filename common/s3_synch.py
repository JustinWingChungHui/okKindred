from django.conf import settings
import boto3


def upload_file_to_s3(filename_and_path):
    '''
    Uploads a file to S3
    '''
    file = str(filename_and_path)

    s3 = boto3.resource('s3')

    data = open(settings.MEDIA_ROOT + file, 'rb')
    s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(Key=file, Body=data)


def remove_file_from_s3(filename_and_path):
    '''
    Removes file from S3
    '''
    file = str(filename_and_path)

    client = boto3.client('s3')
    client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=str(file))


def get_file_from_s3(filename_and_path):
    '''
    Gets a file from S3
    '''
    file = str(filename_and_path)

    client = boto3.client('s3')
    client.download_file(settings.AWS_STORAGE_BUCKET_NAME, file, settings.MEDIA_ROOT + file)

