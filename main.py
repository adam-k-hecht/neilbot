from datetime import datetime
import tweepy
import random
import json
import time

def botaccess(secret):
    with open(secret) as o:
        access = json.load(o)
    return access

def tweepyaccess(keydict):
    auth = tweepy.OAuthHandler(keydict["api-key"], keydict["api-secret"])
    auth.set_access_token(keydict["access-token"], keydict["access-secret"])
    api = tweepy.API(auth)
    return api

def last_tweet_id(api, username):
    for status in tweepy.Cursor(api.user_timeline, id=username).items(1):
        return status.id

def when_last_tweet(api, username):
    for status in tweepy.Cursor(api.user_timeline, id=username).items(1):
        return status.created_at

def main():
    keydict = botaccess("keys.json")
    api = tweepyaccess(keydict)
    my_last = when_last_tweet(api, "NoOneAskedNeil")

    while True:
        neil_last = when_last_tweet(api, "neiltyson")
        last_neil_id = last_tweet_id(api, "neiltyson")
        time.sleep(180)
        if neil_last > my_last:
            new_twt = api.get_status(last_neil_id, tweet_mode='extended')._json['full_text']
            api.update_status("Not that anyone asked me but %s" % (new_twt))
            my_last = when_last_tweet(api, "NoOneAskedNeil")
        else: main()

if __name__ == '__main__':
    main()
