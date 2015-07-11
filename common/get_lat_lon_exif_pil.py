from PIL.ExifTags import TAGS, GPSTAGS
import exifread
'''
From https://gist.github.com/erans/983821

################
# Example ######
################
if __name__ == "__main__":
    image = ... # load an image through PIL's Image object
    exif_data = get_exif_data(image)
    print get_lat_lon(exif_data)

'''
def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()

    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data

def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None

def get_lat_lon(exif_data):
    '''
    Returns the latitude and longitude, if available, from the provided exif_data from PIL
    '''
    lat = 0
    lon = 0

    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_pil_format_to_degrees(gps_latitude)
            if gps_latitude_ref != "N":
                lat = 0 - lat

            lon = _convert_pil_format_to_degrees(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return lat, lon

def _convert_pil_format_to_degrees(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

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


def get_lat_lon_backup(path_name):
    '''
    Opens the file using EXIF Read https://pypi.python.org/pypi/ExifRead
    '''
    # Open image file for reading (binary mode)
    f = open(path_name, 'rb')

    tags = exifread.process_file(f, details=False)

    gps_latitude = _get_if_exist(tags, "GPS GPSLatitude")
    gps_latitude_ref = _get_if_exist(tags, 'GPS GPSLatitudeRef')
    gps_longitude = _get_if_exist(tags, 'GPS GPSLongitude')
    gps_longitude_ref = _get_if_exist(tags, 'GPS GPSLongitudeRef')

    lat = 0
    lon = 0

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = _convert_exif_format_to_degrees(gps_latitude.values)
        if gps_latitude_ref != "N":
            lat = 0 - lat

        lon = _convert_exif_format_to_degrees(gps_longitude.values)
        if gps_longitude_ref != "E":
            lon = 0 - lon

    return lat, lon

