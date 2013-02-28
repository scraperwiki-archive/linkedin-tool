#!/usr/bin/env python
# namestodb.py

import sys

import scraperwiki

"""Take a list of names on stdin (one name per line),
store each name in a sqlite table."""

def main():
    for id,row in enumerate(sys.stdin):
        row = row.strip()
        scraperwiki.sqlite.save(['id'], dict(name=row, id=id), table_name="source")

if __name__ == '__main__':
    main()
