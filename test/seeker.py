import os
import sys
import scraperwiki

from nose.tools import assert_equals, with_setup
from httpretty import HTTPretty, httprettified

from code import seeker

def setup():
  sys.stderr.write('setup()')
  os.system('python code/namestodb.py < people')
  os.system('python code/seeker.py --limit 1')
  scraperwiki.sqlite.execute('DROP TABLE people')
  scraperwiki.sqlite.commit()

@httprettified
def ensure_seeker_finds_people():
  HTTPretty.register_uri(HTTPretty.GET, 'https://api.linkedin.com/v1/people-search:(people:(id,first-name,last-name,headline,distance,num-connections,num-connections-capped,location:(name,country:(code)),industry,positions:(company:(name,type,size,industry,ticker)),public-profile-url,picture-url))?first-name=David&last-name=Blower&oauth2_access_token=fake', open('fixtures/public-results.xml','r').read())
  seeker.do_work(1)
  people = list(scraperwiki.sqlite.select("* from people"))
  assert len(people)
  assert_equals('Mavid Blower', people[0]['name'])


def seeker_only_saves_users_with_full_details():
  with vcr.use_cassette('fixtures/private_people.yaml'):
    seeker.do_work(1)
    people = list(scraperwiki.sqlite.select("* from people"))
    assert_equals('Chris Jones', people[0]['name'])
