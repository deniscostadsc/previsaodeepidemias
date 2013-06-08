import urllib
import json


class OverQueryLimit(Exception):
    pass

GEOCODING_URL = 'http://maps.googleapis.com/maps/api/geocode/json'


def geocoding(**kwargs):
    if 'sensor' not in kwargs:
        kwargs.update({'sensor': 'false'})

    if 'lat' in kwargs and 'lng' not in kwargs or 'lng' in kwargs and 'lat' not in kwargs:
        raise TypeError('You should pass lat and lng!')

    if 'lat' in kwargs:
        lat = kwargs.pop('lat')
        lng = kwargs.pop('lng')
        kwargs.update({'latlng': '%f,%f' % (lat, lng)})

    url = '%s?%s' % (GEOCODING_URL, urllib.urlencode(kwargs))
    response = json.load(urllib.urlopen(url))

    if response['status'] == 'OVER_QUERY_LIMIT':
        raise OverQueryLimit('Google said you are over your quota.')

    address_components = response['results'][0]['address_components']

    interesting_levels = {
        'administrative_area_level_1': 'state',
        'country': 'country',
        'locality': 'city'
    }

    result = {}
    for component in address_components:
        level = list(set(interesting_levels) & set(component['types']))
        if level:
            result[interesting_levels[level[0]]] = component['long_name']

    return result
