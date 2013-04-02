#!/usr/bin/env python
# seeker.py

"""Finds people (from the list in the "source" table).

We expect this script to be run from cron, but you can run it
whenever you like.
"""

from datetime import datetime
import getopt
import json
import sys
import urllib

from lxml import html
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
    do_work(limit)

def do_work(limit):
    #TODO: factor into master dict of colnames/css selectors
    scraperwiki.sql.execute("""CREATE TABLE IF NOT EXISTS
      people (id, source_id, scraped, name, headline, distance,
              num_connections, 
              location_name, location_country_code,
              industry, company_name, company_type,
              company_size, company_industry, company_ticker,
              public_profile_url,
              picture_url)""")
    access_token = json.load(open('access_token.json'))['access_token']
    worklist = scraperwiki.sql.select(
      """source.name AS name, source.id AS source_id
        FROM source LEFT JOIN people
        ON source.id = people.source_id ORDER BY scraped
        LIMIT ?""", [limit])
    for person in worklist:
        params = {
          'keywords': person['name'],
          'oauth2_access_token': access_token
        }
        fields = ("id,first-name,last-name,headline,"+
          "distance,num-connections,num-connections-capped,"+
          "location:(name,country:(code)),industry,"+
          "positions:(company:(name,type,size,industry,ticker)),"+
          "public-profile-url,"+
          "picture-url")
        baseurl = "https://api.linkedin.com/v1/people-search:(people:(%s))" % fields
        r = requests.get(baseurl, params=params)
        save_first_person(source_id=person['source_id'], xml=r.content)
        progress = scraperwiki.sql.select("""count(*) as source,
          (select count(*)from people) as people from source""")
        progress = progress[0]
        message = "Read %(people)d/%(source)d" % progress
        scraperwiki.status('ok', message)

def save_first_person(source_id, xml):
  # open('search-results.xml','w').write(xml)
  doc = html.fromstring(xml)
  for person in doc.cssselect("person"):
      row = dict(
        id = text_or_none('id', person),
        source_id = source_id,
        scraped = datetime.now(),
        name = "%s %s" % (text_or_none('first-name', person), text_or_none('last-name', person)),
        headline = text_or_none('headline', person),
        distance = text_or_none('distance', person),
        num_connections = text_or_none('num-connections', person),
        location_name = text_or_none('location name', person),
        location_country_code = text_or_none('location country code', person),
        industry = text_or_none('industry', person),
        company_name = text_or_none('positions name', person),
        company_type = text_or_none('positions type', person),
        company_size = text_or_none('positions size', person),
        company_industry = text_or_none('positions industry', person),
        company_ticker = text_or_none('positions ticker', person),
        public_profile_url = text_or_none('public-profile-url', person),
        picture_url = text_or_none('picture-url', person)
      )
      if row['id'] not in ['', 'private']:
        scraperwiki.sql.save(['id'], row, 'people')
        break

def text_or_none(selector, doc):
    element = doc.cssselect(selector)
    if len(element) > 0:
      return element[0].text
    else:
      return ''

if __name__ == '__main__':
    main()
