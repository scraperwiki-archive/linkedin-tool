#!/usr/bin/env python
# namestodb.py

import sys
import scraperwiki
import codecs

"""Take a list of names on stdin (one name per line),
store each name in a sqlite table."""

def main():
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    for id,row in enumerate(sys.stdin):
        row = row.strip()
        scraperwiki.sql.save(['id'], dict(name=row, id=id), table_name="source")

if __name__ == '__main__':
    main()
