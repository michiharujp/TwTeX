# coding: utf-8
import requests
import os
import random
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
        print(u"送信に成功しました")
    else:
        print(u"画像の送信に失敗しました")

def url_encode(url):
    url = url.replace('+', '%2B')
    url = url.replace('&', '%26')
    return url

replied = []
mes_list = [u"いい数式テフ！ ちなみにこれが画像テフよ！",
            u"呼んでくれてありがとうテフ！！ 画像を受け取るテフ！",
            u"こんなきれいな数式見せられちゃあ、画像を出せずにはいられないテフ！",
            ]

while 1:
    for tweet in tweepy.Cursor(api.search, q='#texkun').items(1):
        message = mes_list[random.randint(0,len(mes_list)) - 1]
        try:
            print('-----------------------------------')
            print('Tweet by: @' + tweet.user.screen_name)
            print('text is' + tweet.text)
            indexS = tweet.text.find(r'$') + 1
            indexF = tweet.text.find(r'$', indexS)
            formula = tweet.text[indexS: indexF]
            if tweet.id not in replied:
                url = r"http://chart.apis.google.com/chart?cht=tx&chl=" + url_encode(formula)

                message = '@' + tweet.user.screen_name + '\n' + message
                tweet_image(url, message, tweet.id)
                print tweet.user.screen_name + u"さんに" + formula + u"の画像を送ります"
                replied.append(tweet.id)

        except tweepy.TweepError as e:
            print(e.reason)

        except StopIteration:
            break
    sleep(30)
