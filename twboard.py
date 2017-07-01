#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tweepy
#import requests
import yaml
import time

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)


def main():
    auth = tweepy.OAuthHandler(cfg['twitter']['consumer_key'], cfg['twitter']['consumer_secret'])
    auth.set_access_token(cfg['twitter']['access_token'], cfg['twitter']['access_token_secret'])
    api = tweepy.API(auth)
    
    for username in cfg['usernames']:
        user = api.get_user(username)
        count = user.followers_count
        print('{:<30}{:>10}'.format(username, count))

        ts = str(int(time.time()*1000000))+'// followers_count_total{username='+username+'} '+str(count)
        print(ts)



#POST /api/v0/update HTTP/1.1
#Host: host
#X-Warp10-Token: TOKEN
#Content-Type: text/plain


#resp = requests.get('https://todolist.example.com/tasks/')
#if resp.status_code != 200:
#        # This means something went wrong.
#            raise ApiError('GET /tasks/ {}'.format(resp.status_code))
#        for todo_item in resp.json():
#                print('{} {}'.format(todo_item['id'], todo_item['summary']))


#followers_count_total{username=GegAtOvh}




if __name__ == "__main__":
  main()

