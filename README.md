# P4-Streetmap-data-wrangling
Here is the project of data wrangling. The data used in this project is from OpenStreetMap.
This project is to audit map data including streetnames, cities, phones and postal codes in San Jose and keep all these data in the same format.

Then we exported data into csv files and used SQLite to create a database with these files.

We also use SQL queries to demonstrate some outputs.

Here is the link to the data sourse:

https://mapzen.com/data/metro-extracts/metro/san-jose_california/

The raw data file is in the format of osm xml. Here is the download link:

https://s3.amazonaws.com/metro-extracts.mapzen.com/san-jose_california.osm.bz2



audit.py: Audit all the data with key of streetnames, cities, phones and postal codes. It includes update functions of these four types of data.

tocsv.py: It goes over the entire osm file and audit and parse all of them and input to csv files. There are 5 csvs will be created.

tosql.py: Transfer csv to database, which could be searched by sql queries.

sqlimplement.py: sql queries and outcome could be found in report.md as well.

report.md: project presentation.

OSMFILE in audit.py and tocsv.py are both directed to the raw data file locaion.
