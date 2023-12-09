from datetime import datetime
from datetime import timezone
import exifread

def get_lat_lon(path_name):
    '''
    Used to be PIL version, but it was too flakey
    '''
    return get_lat_lon_backup(path_name)

def get_lat_lon_backup(path_name):
    '''
    Opens the file using EXIF Read https://pypi.python.org/pypi/ExifRead
    '''
    # Open image file for reading (binary mode)
    f = open(path_name, 'rb')

    tags = exifread.process_file(f, details=False)

    date_time_original = _get_if_exist(tags, "EXIF DateTimeOriginal")

    gps_latitude = _get_if_exist(tags, "GPS GPSLatitude")
    gps_latitude_ref = _get_if_exist(tags, 'GPS GPSLatitudeRef')
    gps_longitude = _get_if_exist(tags, 'GPS GPSLongitude')
    gps_longitude_ref = _get_if_exist(tags, 'GPS GPSLongitudeRef')

    lat = 0
    lon = 0
    date_time = None

    try:
        #date_time = None
        if date_time_original != None:
            date_time = datetime.strptime(date_time_original.values,"%Y:%m:%d %H:%M:%S").replace(tzinfo=timezone.utc)

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_exif_format_to_degrees(gps_latitude.values)
            if gps_latitude_ref.printable  != "N":
                lat = 0 - lat

            lon = _convert_exif_format_to_degrees(gps_longitude.values)
            if gps_longitude_ref.printable != "E":
                lon = 0 - lon

    except:
        # For when the standards change again... groan
        pass

    f.close()

    return lat, lon, date_time



def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None

def _convert_exif_format_to_degrees(values):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""

    d0 = values[0].num
    d1 = values[0].den
    d = float(d0) / float(d1)

    m0 = values[1].num
    m1 = values[1].den
    m = float(m0) / float(m1)

    s0 = values[2].num
    s1 = values[2].den
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)
