from datetime import datetime
import tweepy
import random
import json
import time
import os

#def botaccess(secret):
#    with open(secret) as o:
#        access = json.load(o)
#    return access

def tweepyaccess():
    CONSUMER_KEY = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
    ACCESS_KEY = os.environ['ACCESS_KEY']
    ACCESS_SECRET = os.environ['ACCESS_SECRET']

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

def last_tweet_id(api, username):
    for status in tweepy.Cursor(api.user_timeline, id=username).items(1):
        return status.id

def when_last_tweet(api, username):
    for status in tweepy.Cursor(api.user_timeline, id=username).items(1):
        return status.created_at

def main():
#    keydict = botaccess("keys.json")
    api = tweepyaccess()
    my_last = when_last_tweet(api, "NoOneAskedNeil")

    while True:
        neil_last = when_last_tweet(api, "neiltyson")
        last_neil_id = last_tweet_id(api, "neiltyson")
        time.sleep(180)
        if neil_last > my_last:
            new_twt = api.get_status(last_neil_id, tweet_mode='extended')._json['full_text']
            api.update_status("Not that anyone asked me but %s" % (new_twt))
            my_last = when_last_tweet(api, "NoOneAskedNeil")

if __name__ == '__main__':
    main()
