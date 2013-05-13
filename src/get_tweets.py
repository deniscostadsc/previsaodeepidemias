#!/usr/bin/env python
# coding: utf-8

from pymongo import Connection
import tweepy

diseases = [
    'dengue',
    'gripe',
    'tuberculose',
    u'cólera',
    u'doença de chagas',
    u'malária',
]

api = tweepy.API()

connection = Connection('localhost', 27017)
db = connection['previsaodeepidemias']
db.raw_tweets.ensure_index('id', unique=True)

raw_tweets = db.raw_tweets


def get_tweets(terms):
    for term in terms:
        tweets = api.search(q=term, rpp=100)
        for tweet in tweets:
            raw_tweets.insert(tweet)

if __name__ == '__main__':
    get_tweets(diseases)
