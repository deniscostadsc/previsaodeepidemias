#!/usr/bin/env python
# coding: utf-8

from pymongo import Connection
import tweepy

def get_tweets(termos):
    api = tweepy.API()
    
    connection = Connection('localhost', 27017)
    
    db = connection['TG']
    
    db.raw_tweets.ensure_index('id', unique=True)
    
    raw_tweets = db.raw_tweets
    
    for termo in termos:
        tweets = api.search(q=termo, rpp=100)
        for tweet in tweets:
            t = {
                'created_at': tweet.created_at,
                'from_user': tweet.from_user,
                'from_user_id': tweet.from_user_id,
                'geo': tweet.geo,
                'id': tweet.id,
                'iso_language_code': tweet.iso_language_code,
                'source': tweet.source,
                'text': tweet.text,
            }
    
            raw_tweets.insert(t)
