from django.conf import settings
import requests
import os, shutil

def get_file_name(target_directory, large_thumbnail):
    return os.path.join(target_directory, str(large_thumbnail).split('/')[-1])


# https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
def download_file(target_directory, large_thumbnail):
    '''
    Downloads remote files for processing
    '''

    url = '{0}{1}'.format(settings.MEDIA_URL, str(large_thumbnail))

    local_filename = get_file_name(target_directory, str(large_thumbnail))
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()

        r.close()
    return local_filename


def clear_directory(directory):
    '''
    Clears the directory recursively of all files and sub directories
    '''

    for the_file in os.listdir(directory):
        file_path = os.path.join(directory, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)