import xml.etree.cElementTree as ET
import pprint
import re


def get_user(element):
    if "uid" in element.attrib:
        return element.attrib["uid"]


def users_id(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if get_user(element) != None:
            users.add(get_user(element))
    return users

def users_count(filename):
    return len(users_id(filename))
