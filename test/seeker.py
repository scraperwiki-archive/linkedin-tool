import os
import vcr

import scraperwiki

from nose.tools import assert_equals

from code import seeker


def setUp():
  os.system('python code/namestodb.py < people')
  os.system('python code/seeker.py --limit 1')
  scraperwiki.sqlite.execute('DROP TABLE people')

def ensure_seeker_finds_people():
  with vcr.use_cassette('fixtures/people.yaml'):
    seeker.do_work(1)
    people = list(scraperwiki.sqlite.select("* from people"))
    assert len(people)
    assert_equals('Mavid Blower', people[0]['name'])

def ensure_seeker_only_saves_users_with_full_details():
  with vcr.use_cassette('fixtures/private_people.yaml'):
    seeker.do_work(1)
    people = list(scraperwiki.sqlite.select("* from people"))
    assert_equals('David Blower', people[0]['name'])
