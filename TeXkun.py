# coding: utf-8
import requests
import os
import tweepy
from time import sleep
from credentials import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def tweet_image(url, message, target_id):
    filename = 'formula.png'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            print(request)
            for chunk in request:
                image.write(chunk)
        api.update_with_media(filename, status=message, in_reply_to_status_id=target_id)
        os.remove(filename)
    else:
        print("Unable to download image")

message = "This is TeX image\n"

replied = []

while 1:
    for tweet in tweepy.Cursor(api.search, q='#showtex').items(3):
        try:
            print('-----------------------------------')
            print('Tweet by: @' + tweet.user.screen_name)
            print('text is' + tweet.text)
            indexS = tweet.text.find(r'$') + 1
            indexF = tweet.text.find(r'$', indexS)
            formula = tweet.text[indexS: indexF]
            if formula != 0 and not tweet.id in replied:
                url = r"http://chart.apis.google.com/chart?cht=tx&chl=" + formula

                tweet_image(url, message, tweet.id)
                replied = replied.append(tweet.id)
        except tweepy.TweepError as e:
            print(e.reason)

        except StopIteration:
            break
    sleep(300)
