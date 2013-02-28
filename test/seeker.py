import os

import scraperwiki

def setUp():
  os.system('python code/namestodb.py < people')
  os.system('python code/seeker.py --limit 1')
  scraperwiki.sqlite.execute('DROP TABLE people')

def ensure_seeker_find_people():
  people = list(scraperwiki.sqlite.select("* from people"))
  assert people
