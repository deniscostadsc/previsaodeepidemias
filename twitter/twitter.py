# coding: utf-8

from pymongo import Connection
import tweepy

doencas = ['dengue', u'malária']

api = tweepy.API()

connection = Connection('localhost', 27017)

db = connection['TG']

db.raw_tweets.ensure_index('id', unique=True)

raw_tweets = db.raw_tweets

for doenca in doencas:
    tweets = api.search(q=doenca, rpp=100)
    for tweet in tweets:
        t = {
            'created_at': tweet.created_at,
            'id': tweet.id,
            'from_user_id': tweet.from_user_id,
            'text' : tweet.text,
            'geo': tweet.geo,
        }

        raw_tweets.insert(t)
