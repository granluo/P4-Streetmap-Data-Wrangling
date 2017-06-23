import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict
import main

def iscity (cityname):
    try:
        int(cityname)
        return False
    except ValueError:
        return True


filename = main.getfile()
tagattrib = defaultdict(set)
postcodeset = defaultdict(set)
cities = set()


for _, element in ET.iterparse(filename):
    for att in element.attrib:
        tagattrib[element.tag].add(att)
    if element.tag == "node":
        city = "not mentioned"
        postcode = None
        for ele in element:
            if ele.attrib['k'] == "addr:city":
                city = ele.attrib['v']
                cities.add(city)
            if not iscity(city):
                print ele.attrib
            if ele.attrib['k'] == "addr:postcode":
                postcode = ele.attrib['v']

        if postcode is not None:
            postcodeset[city].add(postcode)



pprint.pprint(dict(postcodeset))
pprint.pprint(cities)
#


# pprint.pprint(dict(tagattrib))
