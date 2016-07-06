
from geopy.geocoders import GoogleV3

def geo_lat_long_eval(cleaned_data):
    # departure
    data = {}
    departure_location = cleaned_data.get('departure_location')
    zip_code = cleaned_data.get('zip_code')
    departure_street = cleaned_data.get('departure_street', '')

    # destiny
    destiny_location = cleaned_data.get('destiny_location')
    destiny_zip_code = cleaned_data.get('destiny_zip_code')
    destiny_street = cleaned_data.get('destiny_street', '')

    geolocator = GoogleV3()
    departure_loc = geolocator.geocode("{} {} {}".format(zip_code, departure_location, departure_street))
    destiny_loc = geolocator.geocode("{} {} {}".format(destiny_zip_code, destiny_location, destiny_street))

    try:
        departure_loc.latitude
        departure_dict = {
            'lat': departure_loc.latitude,
            'long': departure_loc.longitude,
        }
        data.update(departure_dict)
    except AttributeError:
        return "Leider ist ein Fehler in der Abfahrtsortadresse.", False

    try:
        destiny_loc.latitude
        destiny_dict = {
            'destiny_lat': destiny_loc.latitude,
            'destiny_long': destiny_loc.longitude,
        }
        data.update(destiny_dict)
    except AttributeError:
        return "Leider ist ein Fehler in der Zielortadresse.", False

    return data, True