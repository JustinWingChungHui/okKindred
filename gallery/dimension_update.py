from django.conf import settings
from common.s3_synch import get_file_from_s3
from PIL import Image
import MySQLdb
import os

'''
This is to set the missing dimension records for all gallery images.  Run this within Django shell
'''

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# Create new connection
db_settings = settings.DATABASES['default']
try:
    connection = MySQLdb.connect(host=db_settings['HOST'],db=db_settings['NAME'],user=db_settings['USER'],passwd=db_settings['PASSWORD'])
except MySQLdb.OperationalError as e:
    connection = None

# Get all records without  image dimensions
with connection.cursor() as cursor:
    cursor.execute("SELECT id, thumbnail, large_thumbnail, original_image FROM gallery_image where thumbnail_width is null;")
    results = dictfetchall(cursor)


for row in results:

    exists = True

    # Download files from s3 and open with pillow
    try:
        print("getting: " + row['thumbnail'])
        get_file_from_s3(row['thumbnail'])
    except:
        exists = False

    if exists:
        thumbnail = Image.open(settings.MEDIA_ROOT + row['thumbnail'])

        print("getting: " + row['large_thumbnail'])
        get_file_from_s3(row['large_thumbnail'])
        large_thumbnail = Image.open(settings.MEDIA_ROOT + row['large_thumbnail'])

        print("getting: " + row['original_image'])
        get_file_from_s3(row['original_image'])
        original_image = Image.open(settings.MEDIA_ROOT + row['original_image'])

        # Construct update statement
        print('Updating...')
        sql = """UPDATE gallery_image
                set thumbnail_width = {},
                thumbnail_height = {},
                large_thumbnail_width = {},
                large_thumbnail_height = {},
                original_image_width = {},
                original_image_height = {}
                where id = {};""".format(thumbnail.size[0], thumbnail.size[1], large_thumbnail.size[0], large_thumbnail.size[1], original_image.size[0], original_image.size[1],row['id'])
        print(sql)

        #Execute sql update statement
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()

        # Delete downloaded files
        print('deleting files')
        os.remove(settings.MEDIA_ROOT + row['thumbnail'])
        os.remove(settings.MEDIA_ROOT + row['large_thumbnail'])
        os.remove(settings.MEDIA_ROOT + row['original_image'])

    else:

        # Construct delete tag statement
        print('Updating...')
        sql = """DELETE FROM gallery_tag WHERE image_id = {};""".format(row['id'])
        print(sql)

        #Execute sql delete tag statement
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()

        # Construct delete statement
        print('Updating...')
        sql = """DELETE FROM gallery_image WHERE id = {};""".format(row['id'])
        print(sql)

        #Execute sql delete statement
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()


