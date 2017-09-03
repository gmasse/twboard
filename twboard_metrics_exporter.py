#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import requests
import yaml
import json
import time

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)


def main():
    auth = tweepy.OAuthHandler(cfg['twitter']['consumer_key'], cfg['twitter']['consumer_secret'])
    auth.set_access_token(cfg['twitter']['access_token'], cfg['twitter']['access_token_secret'])
    api = tweepy.API(auth)
   
    timestamp=int(time.time()*1000)

    data=[]
    for username in cfg['usernames']:
        user = api.get_user(username)
        count = user.followers_count

        ts={
            'metric': 'followers_count_total',
            'timestamp': timestamp,
            'value': count,
            'tags': { 'username': username }
        }
        data.append(ts)
        print('{:<30}{:>10}'.format(username, count))

    print json.dumps(data)

    url = cfg['metrics']['url']+'/api/put'
    resp = requests.post(url, json=data, auth=('twboardbot', cfg['metrics']['write_token']))

    if resp.status_code != 204:
        # This means something went wrong.
        print('ERROR: POST /api/put {}'.format(resp.status_code))


if __name__ == "__main__":
  main()

