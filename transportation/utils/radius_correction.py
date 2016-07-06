
CITY_RADIUS = {
    'Berlin': 15,
    'München': 10,
    'Stuttgart': 10,
    'Köln': 15,
    'Leipzig': 10,
    'Else': 8,
}

def add_km_to_radius(radius, city):
    if city in CITY_RADIUS:
        km = CITY_RADIUS.get(city)
    else:
        km = CITY_RADIUS.get('Else')

    new_radius = radius + km
    print("----------- km to add: {} ------------".format(km))
    print("----------- New radius: {} ------------".format(new_radius))

    return new_radius