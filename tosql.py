import sqlite3
import csv
from pprint import pprint

sqlite_file = "mydb.db"

conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()

cur.executescript('''
    DROP TABLE IF EXISTS nodes_tags;
    DROP TABLE IF EXISTS nodes;
    DROP TABLE IF EXISTS ways_nodes;
    DROP TABLE IF EXISTS ways;
    DROP TABLE IF EXISTS ways_tags;
''')
conn.commit()

cur.executescript('''
    CREATE TABLE nodes_tags(id INTEGER, key TEXT, value TEXT,type TEXT);
    CREATE TABLE nodes( id INTEGER, lat REAL, lon REAL, user TEXT, uid integer, version INTEGER, changeset INTEGER, timestamp TEXT);
    CREATE TABLE ways_nodes(id INTEGER, node_id, INTEGER, position INTEGER);
    CREATE TABLE ways(id INTEGER, user TEXT, uid INTEGER, version TEXT, timestamp TEXT, changeset INTEGER);
    CREATE TABLE ways_tags(id INTEGER, key TEXT, value TEXT,type TEXT )
''')
conn.commit()



with open('nodes_tags.csv','rb') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db_nodes_tags = [(i['id'], i['key'],i['value'].decode("utf-8"), i['type']) for i in dr]

with open('nodes.csv','rb') as fin:
    dr = csv.DictReader(fin)
    to_db_nodes =  [(i['id'], i['lat'],i['lon'],i['user'].decode("utf-8"),i['uid'].decode('utf-8'),i['version'],i['changeset'], i['timestamp']) for i in dr]

with open ('ways_nodes.csv', 'rb') as fin:
    dr = csv.DictReader(fin)
    to_db_ways_nodes = [(i['id'], i['node_id'],i['position']) for i in dr]

with open ('ways.csv', 'rb') as fin:
    dr = csv.DictReader(fin)
    to_db_ways = [(i['id'],i['user'].decode("utf-8"),i['uid'],i['version'].decode("utf-8"),i['timestamp'].decode("utf-8"), i['changeset']) for i in dr]

with open('ways_tags.csv','rb') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db_ways_tags = [(i['id'], i['key'],i['value'].decode("utf-8"), i['type'].decode("utf-8")) for i in dr]


# insert the formatted data
cur.executemany("INSERT INTO nodes_tags(id, key, value,type) VALUES (?, ?, ?, ?);", to_db_nodes_tags)
cur.executemany("INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db_nodes)
cur.executemany("INSERT INTO ways_nodes(id, node_id, position) VALUES (?, ?, ?);", to_db_ways_nodes)
cur.executemany("INSERT INTO ways(id, user, uid, version, timestamp, changeset) VALUES (?, ?, ?, ?, ?, ?);", to_db_ways)
cur.executemany("INSERT INTO ways_tags(id, key, value, type) VALUES (?, ?, ?, ?);", to_db_ways_tags)

# commit the changes
conn.commit()
cur.execute('SELECT * FROM ways_tags where key = "city" AND value LIKE "San Jo$" AND value <> "San Jose"')
all_rows = cur.fetchall()
print('1):')
pprint(all_rows)
conn.close()
