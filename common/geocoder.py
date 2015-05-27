from geopy.geocoders import GoogleV3
from geopy.geocoders import Bing
from django.conf import settings


def geocode_address(address):
    '''
    Gets the longitude and latitude of address for plotting on a map
    '''
    if not address:
        return

    #Attempt to google the location, if it fails, try bing as backup
    try:

        google_locator = GoogleV3(api_key = settings.GOOGLE_API_KEY)
        location = google_locator.geocode(address)


        if location.latitude == 0 and location.longitude ==0:
            return _geocode_address_using_backup()

        return location

    except:
        return _geocode_address_using_backup()


def _geocode_address_using_backup(address):
    '''
    Gets the logitude and latitude of address for plotting on a map from backup service (Bing)
    '''
    try:
        bing_locator = Bing(api_key = settings.BING_MAPS_API_KEY)

        return bing_locator.geocode(address)
    except:
        return