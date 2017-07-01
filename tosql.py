import sqlite3
import csv
from pprint import pprint

sqlite_file = "mydb.db"

conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()

cur.execute('''
    DROP TABLE IF EXISTS nodes_tags
''')
conn.commit()

cur.execute('''
    CREATE TABLE nodes_tags(id INTEGER, key TEXT, value TEXT,type TEXT)
''')
conn.commit()

with open('nodes_tags.csv','rb') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'], i['key'],i['value'].decode("utf-8"), i['type']) for i in dr]

# insert the formatted data
cur.executemany("INSERT INTO nodes_tags(id, key, value,type) VALUES (?, ?, ?, ?);", to_db)
# commit the changes
conn.commit()
cur.execute('SELECT * FROM nodes_tags where key == "phone"')
all_rows = cur.fetchall()
print('1):')
pprint(all_rows)
conn.close()
