import urllib
import json

GEOCODING_URL = 'http://maps.googleapis.com/maps/api/geocode/json'


def geocoding(**kwargs):
    kwargs.update({'sensor': 'false'})

    if 'lat' in kwargs and 'lng' not in kwargs or 'lng' in kwargs and 'lat' not in kwargs:
        raise TypeError('You should pass lat and lng!')

    if 'lat' in kwargs:
        lat = kwargs.pop('lat')
        lng = kwargs.pop('lng')
        kwargs.update({'latlng': '%s,%s' % (str(lat), str(lng))})

    url = '%s?%s' % (GEOCODING_URL, urllib.urlencode(kwargs))
    response = json.load(urllib.urlopen(url))

    result = []
    leves = ['locality', 'administrative_area_level_1', 'country']
    for component in response['results'][0]['address_components']:
        if list(set(leves) & set(component['types'])):
            result.append(component['long_name'])
    return ', '.join(result)
