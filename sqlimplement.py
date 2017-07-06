#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import csv
from pprint import pprint

sqlite_file = "mydb.db"

conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()

cur.execute('''UPDATE nodes_tags
SET value = "San Jose"
WHERE nodes_tags.value like  'San Jos%' AND nodes_tags.key = 'city' and nodes_tags.value <> 'San Jose';
''')
cur.execute('''UPDATE ways_tags
SET value = "San Jose"
WHERE ways_tags.value like  'San Jos%' AND ways_tags.key = 'city' and ways_tags.value <> 'San Jose';
''')
cur.execute('SELECT * FROM nodes_tags LIMIT 10')
pprint(cur.fetchall())
cur.execute('SELECT * FROM nodes LIMIT 10')
pprint(cur.fetchall())
cur.execute('SELECT * FROM ways LIMIT 10')
pprint(cur.fetchall())
cur.execute('SELECT * FROM ways_nodes LIMIT 10')
pprint(cur.fetchall())
cur.execute('SELECT * FROM ways_tags LIMIT 10')

all_rows = cur.fetchall()
pprint(all_rows)
cur.executescript('')

cur.execute('SELECT tags.value, COUNT(*) as count \
FROM (SELECT * FROM nodes_tags \
	  UNION ALL \
      SELECT * FROM ways_tags) as tags \
WHERE tags.key="postcode" \
GROUP BY tags.value \
ORDER BY count DESC \
limit 10;\
')
pprint(cur.fetchall())

cur.execute('SELECT tags.value, COUNT(*) as count \
FROM (SELECT * FROM nodes_tags \
	  UNION ALL \
      SELECT * FROM ways_tags) as tags \
WHERE tags.key="city" \
GROUP BY tags.value \
ORDER BY count DESC; \
')
pprint(cur.fetchall())
# for items in cur.fetchall():
#     print ''
#     for item in items:
#         print item, ', '
# all_rows = cur.fetchall()
# pprint (all_rows)
# pprint(cur.fetchall())

#
# cur.execute("SELECT * \
# FROM (SELECT * FROM nodes_tags \
# 	  UNION ALL \
#       SELECT * FROM ways_tags) tags \
# WHERE tags.value like  'San Jos%' AND tags.key = 'city' and tags.value <> 'San Jose';\
# ")


# all_rows = cur.fetchall()

# names = [description[0] for description in cur.description()]
# # print '\n',names
# for items in cur.fetchall():
#     print ''
#     for item in items:
#         print item, ', ',
#
# pprint(cur.fetchall())
#
#
# cur.execute("SELECT * \
# FROM (SELECT * FROM nodes_tags \
# 	  UNION ALL \
#       SELECT * FROM ways_tags) tags \
# WHERE tags.value like  'San Jos%' AND tags.key = 'city' and tags.value <> 'San Jose';\
# ")
#
# pprint(cur.fetchall())
# cur.execute("SELECT * \
# FROM (SELECT * FROM nodes_tags \
# 	  UNION ALL \
#       SELECT * FROM ways_tags) tags \
# WHERE tags.value like  'San Jos';\
# ")

#
# cur.execute('UPDATE tags\
# FROM (SELECT * FROM nodes_tags \
# 	  UNION ALL \
#       SELECT * FROM ways_tags) as tags \
# SET value ="San Jose" \
# WHERE value = San Jos\xe9 ; \
#  ')
conn.close()
