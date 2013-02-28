#!/usr/bin/env python
# seeker.py

"""Finds people (from the list in the "source" table).

We expect this script to be run from cron, but you can run it
whenever you like.
"""

import getopt
import json
import sys
import urllib

import requests
import scraperwiki

def main(argv=None):
    if argv is None:
        argv = sys.argv
    opts, args = getopt.getopt(argv[1:], '', ['limit='])
    limit = 100
    for k,v in opts:
        if k == '--limit':
            limit = int(v)
    scraperwiki.sqlite.execute("""CREATE TABLE IF NOT EXISTS 
      people (id, scraped)""")

    do_work(limit)

def do_work(limit):
    access_token = json.load(open('access_token.json'))['access_token']
    worklist = scraperwiki.sqlite.select(
      """* FROM source LEFT JOIN people
        ON source.id = people.id ORDER BY scraped
        LIMIT ?""", [limit])
    for person in worklist:
        firstname = person['name'].split()[0]
        lastname = person['name'].split()[-1]
        params = {
          'first-name': firstname,
          'last-name': lastname,
          'oauth2_access_token': access_token
        }
        fields = ("id,first-name,last-name,headline,"+
          "distance,num-connections,num-connections-capped,"+
          "location:(name,country:(code)),industry,"+
          "positions:(company:(name,type,size,industry,ticker)),"+
          "public-profile-url,"+
          "picture-url")
        baseurl = "https://api.linkedin.com/v1/people-search:(people:(%s))" % fields
        url = baseurl + '?' + urllib.urlencode(params)
        r = requests.get(url)
        xml = r.text
        print xml

if __name__ == '__main__':
    main()
