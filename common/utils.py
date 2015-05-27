from django.db import connection
import random
import hashlib


def get_file_size(file):
    '''
    Gets the file size
    '''
    file.seek(0, 2)  # Seek to the end of the file
    size = file.tell()  # Get the position of EOF
    file.seek(0)  # Reset the file position to the beginning
    return size

def query_to_dicts(query_string, *query_args):
    '''
    Retrieve a list of dictionaries with keys for the column values.
    '''
    cursor = connection.cursor()
    cursor.execute(query_string, query_args)
    col_names = [desc[0] for desc in cursor.description]

    while True:
        row = cursor.fetchone()

        if row is None:
            break

        row_dict = dict(zip(col_names, row))
        yield row_dict

    return

def create_hash(seed_string):
    '''
    Creates a hash string to use in secure stuff
    '''
    bits = [seed_string] + [str(random.SystemRandom().getrandbits(512))]
    return hashlib.sha256("".join(bits).encode("utf-8")).hexdigest()