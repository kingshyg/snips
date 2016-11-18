# -*- coding: utf-8 -*-
import os
import sys

import json

import unicodecsv as csv
import requests

TOKEN = os.getenv("FEED_WRANGLER")
if TOKEN is None:
    print "NO TOKEN!!!"
    sys.exit()

URL = "https://feedwrangler.net/api/v2/feed_items/list"
MAX_LIMIT = 100

def main(filename):

    feed_names = {}
    starred = {}
    total_star = 0

    # loop till we don't have the item-limit that we set
    while True:
        feed_data = {
            "access_token": TOKEN,
            "starred": "true",
            "offset": total_star,
            "limit": MAX_LIMIT
        }

        resp = requests.get(URL, data=feed_data)

        feed_items = json.loads(resp.text)['feed_items']
        for item in feed_items:
            feed_id = item['feed_id']

            feed_names.setdefault(
                feed_id, {'name': item['feed_name'], 'count': 0})

            feed_names[feed_id]['count'] += 1

            starred.setdefault(feed_id, [])
            starred[feed_id].append({
                "id": item['feed_item_id'],
                "updated": item['updated_at'],
                "feed_id": feed_id,
                "title": item['title'],
                "url": item['url']
            })

        num_items = len(feed_items)
        total_star += num_items

        print "total starred items = %d" % total_star

        if num_items < MAX_LIMIT:
            break

    for key, val in feed_names.items():
        print "%d\t%d\t%s" % (key, val['count'], val['name'])

    filep = open(filename, 'wb')
    writer = csv.writer(filep)
    for key, val in starred.items():
        for item in val:
            writer.writerow(item.values())
    filep.close()

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print "Usage: ./feed.py <filename.csv>"
        sys.exit(1)

    main(sys.argv[1])
