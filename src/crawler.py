#!/usr/bin/env python
# coding: utf-8

import thread

from pymongo import Connection
import tweepy

from maps.geocoding import geocoding

diseases = [
    'dengue',

    'gripe',
    'gripado',
    'gripada',

    'tuberculose',

    u'cólera',
    'colera',

    u'malária',
    'malaria'
]

api = tweepy.API()

connection = Connection('localhost', 27017)
db = connection['previsaodeepidemias']
db.raw_tweets.ensure_index('id', unique=True)

raw_tweets = db.raw_tweets


def geocode_and_save(tweet):
    if tweet.geo:
        lat = tweet.geo['coordinates'][0]
        lng = tweet.geo['coordinates'][1]

        if lat and lng:
            location = geocoding(lat=lat, lng=lng)

            location_str = ', '.join(
                [location[level] for level in 'city state country'.split() if level in location]
            )

            json = {
                'created_at': tweet.created_at,
                'from_user': tweet.from_user,
                'from_user_id': tweet.from_user_id,
                'from_user_id_str': tweet.from_user_id_str,
                'from_user_name': tweet.from_user_name,
                'geo': tweet.geo,
                'id': tweet.id,
                'id_str': tweet.id_str,
                'iso_language_code': tweet.iso_language_code,
                'location': location,
                'location_str': location_str,
                'profile_image_url': tweet.profile_image_url,
                'profile_image_url_https': tweet.profile_image_url_https,
                'source': tweet.source,
                'text': tweet.text
            }
            raw_tweets.insert(json)


def get_tweets(terms):
    for term in terms:
        tweets = api.search(q=term, rpp=100)
        for tweet in tweets:
            thread.start_new_thread(geocode_and_save, (tweet,))

if __name__ == '__main__':
    get_tweets(diseases)
