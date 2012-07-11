# coding: utf-8

from pymongo import Connection
import tweepy

doencas = ['dengue', u'malária']

api = tweepy.API()

connection = Connection('localhost', 27017)

raw_tweets_db = connection['raw_tweets']

posts = raw_tweets_db.posts

for doenca in doencas:
    tweets = api.search(q=doenca, rpp=100)
    for tweet in tweets:
        t = {
            'created_at': tweet.created_at,
            'from_user_id': tweet.from_user_id,
            'text' : tweet.text,
            'geo': tweet.geo,
        }

        posts.insert(t)
