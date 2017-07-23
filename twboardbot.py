#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop
import requests
import yaml
import json
from operator import itemgetter

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)


def twstat(weeks_ago= 3):
    hours_ago = 24*7*weeks_ago

    query = { "queries": [ { "metric": "followers_count_total" } ] }
    url = cfg['metrics']['url']+'/api/query/last'
    resp = requests.post(url, json=query, auth=('twboardbot', cfg['metrics']['read_token']))

    stats = {}
    if resp.status_code != 200:
        # This means something went wrong.
        print('ERROR: POST /api/query/last {}'.format(resp.status_code))
    else:
        unsorted_list = [(item['tags']['username'], int(float(item['value']))) for item in resp.json()]
        for (username, count) in unsorted_list:
            stats[username] = { 'now': count }

    query = { "start": str(hours_ago)+"h-ago", "end": str(hours_ago-24)+"h-ago", "queries": [ { "metric": "followers_count_total", "aggregator": "max", "tags": { "username": "*" }} ] }
    url = cfg['metrics']['url']+'/api/query'
    resp = requests.post(url, json=query, auth=('twboardbot', cfg['metrics']['read_token']))

    if resp.status_code != 200:
        # This means something went wrong.
        print('ERROR: POST /api/query {}'.format(resp.status_code))
    else:
        for item in resp.json():
            username = item['tags']['username']
            dps = item['dps']
            first_timestamp = sorted(dps)[0]
            stats[username][str(weeks_ago)+'w-ago'] = int(float(dps[first_timestamp]))
            stats[username]['Δ-'+str(weeks_ago)+'w'] = stats[username]['now'] - stats[username]['3w-ago']

    output = ''
    key='Δ-'+str(weeks_ago)+'w'
    unsorted_list = [(item[0], item[1][key]) for item in stats.items()]
    sorted_list = sorted(unsorted_list, key=itemgetter(1), reverse=True)
    output += '{:<15}{:>4}{:>5}'.format('@username', key, 'now')
    output += "\n"
    output += '-'*24
    output += "\n"
    for (username, value) in sorted_list:
        output += '{:<15}{:>4}{:>5}'.format(username, stats[username][key], stats[username]['now'])
        output += "\n"

    return output


async def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type != 'text':
        return

    command = msg['text'].lower()

    if command == '/followers':
        output = '<pre>'
        output += twstat(3)
        output += '</pre>'
        print(output)

        await bot.sendMessage(chat_id, output, parse_mode='HTML')


def main():
    global bot

    bot = telepot.aio.Bot(cfg['telegram']['token'])
    loop = asyncio.get_event_loop()

    loop.create_task(MessageLoop(bot, handle).run_forever())
    print('Listening ...')

    loop.run_forever()



if __name__ == "__main__":
  main()

