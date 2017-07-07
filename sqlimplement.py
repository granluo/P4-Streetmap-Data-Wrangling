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
# cur.execute('SELECT * FROM nodes_tags LIMIT 10')
# pprint(cur.fetchall())
# cur.execute('SELECT * FROM nodes LIMIT 10')
# pprint(cur.fetchall())
# cur.execute('SELECT * FROM ways LIMIT 10')
# pprint(cur.fetchall())
# cur.execute('SELECT * FROM ways_nodes LIMIT 10')
# pprint(cur.fetchall())
# cur.execute('SELECT * FROM ways_tags LIMIT 10')
#
# all_rows = cur.fetchall()
# pprint(all_rows)
# cur.executescript('')

# This function is to print outcome of quesries in a table format.
def outcomeprint(cursor,space = 15):
	all_rows = cursor.fetchall()
	title =  [(description[0]) for description in cursor.description]
	row_format =("{:<"+str(space) + "}") * (len(title))
	print row_format.format(*title)
	for i in all_rows:
		for j in i:
			print ("{:<"+str(space) + "}") .format(j),
		print ''
	print ''

cur.execute('SELECT tags.value, COUNT(*) as count \
FROM (SELECT * FROM nodes_tags \
	  UNION ALL \
      SELECT * FROM ways_tags) as tags \
WHERE tags.key="postcode" \
GROUP BY tags.value \
ORDER BY count DESC \
limit 10;\
')
outcomeprint(cur)

cur.execute('SELECT tags.value, COUNT(*) as count \
FROM (SELECT * FROM nodes_tags \
	  UNION ALL \
      SELECT * FROM ways_tags) as tags \
WHERE tags.key="city" \
GROUP BY tags.value \
ORDER BY count DESC; \
')

outcomeprint(cur)

# find out the number of unique users
cur.execute('SELECT COUNT(DISTINCT(e.uid)) AS Count_of_users\
		FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;')

outcomeprint(cur)

# number of nodes
cur.execute('SELECT COUNT(*) as Number_of_Nodes FROM nodes;')
outcomeprint(cur)

# number of ways
cur.execute('SELECT COUNT(*) as Number_of_Ways FROM ways;')
outcomeprint(cur)

# Top 10 contributing users
cur.execute('''SELECT e.user as User, COUNT(*) as Number_of_Contributions
        FROM (SELECT user FROM Nodes UNION ALL SELECT user FROM Ways) e
        GROUP BY e.user
        ORDER BY Number_of_Contributions DESC
        LIMIT 10;
		''')
outcomeprint(cur)

# Number of users appearing only once (having 1 post)

cur.execute('''SELECT count(*) as first_time_contribution_user
FROM 	(select e.user,count(*) as count
		From (select user from nodes union all select user from ways) e
		group by e.user
		having count = 1);

''')
outcomeprint(cur)

# Most popular cruisines

cur.execute('''
SELECT nodes_tags.value, COUNT(*) as num
        FROM nodes_tags
            JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='restaurant') i
            ON nodes_tags.id=i.id
        WHERE nodes_tags.key='cuisine'
        GROUP BY nodes_tags.value
        ORDER BY num DESC
        LIMIT 10;

''')
outcomeprint(cur)

cur.execute('''
	SELECT nodes_tags.value, count(*) as num
	FROM nodes_tags
	GROUP BY nodes_tags.value
	ORDER BY num DESC
	limit 15
''')
outcomeprint(cur)
cur.execute('''
	SELECT nodes_tags.key, nodes_tags.value, count(*) as num
	FROM nodes_tags
	where value like '%parking%'
	GROUP BY nodes_tags.value
	ORDER BY num DESC
	limit 40
''')
outcomeprint(cur,35)

cur.execute('''

''')
conn.close()
