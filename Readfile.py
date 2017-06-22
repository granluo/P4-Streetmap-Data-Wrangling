import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint

DATASETLOC = "C:\Users\Zongran\Dropbox\Udacity nano\p4 streetmap data wrangling dataset\san-jose_california.osm"
tagstat = defaultdict(int)

count = 0
for event,ele in ET.iterparse (DATASETLOC,events= ('start',)):

#    if  [child for child in ele]:
    #    print [child.tag for child in ele]
    # try:
    tagstat[ele.tag] += 1
    # except:
    #     tagstat[ele.tag] = 1

    count += 1
    if count >= 1000:
        break
print tagstat
