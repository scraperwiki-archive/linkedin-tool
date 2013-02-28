import os

import scraperwiki
import vcr

def setUp():
  os.system('python code/namestodb.py < people')
  os.system('python code/seeker.py --limit 1')
  scraperwiki.sqlite.execute('DROP TABLE people')

def ensure_seeker_find_people():
  with vcr.use_cassette('fixtures/people.yaml'):
    from code import seeker
    seeker.do_work(1)
    people = list(scraperwiki.sqlite.select("* from people"))
    assert len(people)
