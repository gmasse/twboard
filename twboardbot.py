#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import yaml
import json
from operator import itemgetter

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)


def main():

    query = { "queries": [ { "metric": "followers_count_total" } ] }

    url = cfg['metrics']['url']+'/api/query/last'
    resp = requests.post(url, json=query, auth=('twboardbot', cfg['metrics']['read_token']))

    if resp.status_code != 200:
        # This means something went wrong.
        print('ERROR: POST /api/query/last {}'.format(resp.status_code))
    else:
        unsorted_list = [(item['tags']['username'], int(float(item['value']))) for item in resp.json()]
        sorted_list = sorted(unsorted_list, key=itemgetter(1), reverse=True)

        for (username, count) in sorted_list:
            print('{:<30}{:>10}'.format(username, count))




if __name__ == "__main__":
  main()

