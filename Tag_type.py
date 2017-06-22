import xml.etree.cElementTree as ET
import pprint
import re
import Tag_counts
import sys

sys.dont_write_bytecode = True
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        if not (lower.match(element.attrib['k']) is None):
            keys["lower"] += 1
            #print lower.match(element.attrib['k']).group(0)
        elif not  (lower_colon.match(element.attrib['k']) is None):
            keys["lower_colon"] += 1
            #print lower_colon.match(element.attrib['k']).group(0)
        elif not (problemchars.match(element.attrib['k']) is None):
            keys["problemchars"] += 1
            #print problemchars.match(element.attrib['k']).group(0)
        else:
            keys["other"] += 1

        #print element.attrib['k']

    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename,events=("start","end")):
        # if _ == "start":
        #     print element.tag
        #     if element.tag == "node":
        #         print [child.tag for child in element]
        #         for child in element:
        #             print child.attrib
        #     print [rows.tag for rows in element]
        keys = key_type(element, keys)
    return keys
