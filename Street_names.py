"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
city_type_re = re.compile('.*')
phone_type_re = re.compile(r'\+1\s\d{3}\s\d{3}\s\d{4}')
postcode_type_re = re.compile(r'\d{5}$')

city_expected = ["Santa Clara","San Jose","Sunnyvale","Saratoga",'Mountain View','Alviso','Campbell','Cupertino','Felton','Los Gatos','Milpitas','Moffett Field','Morgan Hill','Mt Hamilton']
# UPDATE THIS VARIABLE


city_mapping = { "SUnnyvale": "Sunnyvale",
            "San Jos\xe9": "San Jose",
            "Ave": "San Jose",
            "san jose": "San Jose",
            }

street_expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons","Way","Terrace","Row","Plaza", "Circle", "Loop", "Hill", "Expressway", "Court"]
# UPDATE THIS VARIABLE


street_mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd": "Road",
            "Rd.": "Road",
            "Ln": "Lane",
            "court": "Court",
            "Blvd": "Boulevard",
            "Dr": "Drive"
            }
def get_mapping():
    return mapping

def audit_street_type(street_types, street_name,type_data):
    m = None
    if type_data == "street":
        m = street_type_re.search(street_name)
        expected = street_expected
    elif type_data == "city":
        m = city_type_re.search(street_name)
        expected = city_expected

    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

    if type_data == "phone":
        m = phone_type_re.match(street_name)
        if m:
            street_types['regular'].add(street_name)
        else:
            street_types['others'].add(street_name)
    if type_data == "postcode":
        m = postcode_type_re.match(street_name)
        if m:
            street_types['5digits'].add(street_name)
        else:
            street_types['others'].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def is_city_name(elem):
    return (elem.attrib['k'] == "addr:city")

def is_phone_number(elem):
    return ("phone" in elem.attrib['k'])

def is_postcode_number(elem):
    return ("postcode" in elem.attrib['k'])

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    city_types = defaultdict(set)
    phonenum_types = defaultdict(set)
    postcode_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'], "street")
                elif is_city_name(tag):
                    audit_street_type(city_types, tag.attrib['v'], "city")
                elif is_phone_number(tag):
                    audit_street_type(phonenum_types, tag.attrib['v'],"phone")
                elif is_postcode_number(tag):
                    audit_street_type(postcode_types,tag.attrib['v'],"postcode")

    osm_file.close()
    return (postcode_types,phonenum_types,city_types,street_types)#{"street":street_types,"city":city_types}


def update_name(name):
    name_array = name.split(' ')
    last = name_array[-1]
    name_array[-1] = street_mapping[last]
    return ' '.join(name_array)

def update_city_name(name):
    return city_mapping[name]

def update_phone_num(num):
    m = phone_type_re.match(num)
    keypad = {'2':'ABCabc','3':'DEFdef','4':'GHIghi','5':'JKLjkl','6':'MNOmno','7':'PQRSpqrs','8':'TUVtuv','9':'WXYZwxyz'}
    if m is None:
        if re.search(r'[a-zA-Z]',num) is not None:
            for key in keypad:
                num = re.sub(r'['+keypad[key]+']',key,num)
        if '-' in  num:
            num = re.sub('-','',num)
        if '.' in num:
            num = re.sub('\.','',num)
        if '(' in num or ')' in num:
            num = re.sub('[()]','',num)
        num = re.sub('\s+','',num)
        if re.match(r'\d{10}',num) is not None:
            num = num[:3] + ' ' + num[3:6] + ' ' +num[6:]
        if re.match(r'\d{11}',num) is not None:
            num = num[:1] + ' ' + num[1:4] + ' ' + num[4:7] + ' ' +num[7:]
        if re.match(r'\d{3}\s\d{3}\s\d{4}', num):
            num = '+1 ' +num
        if re.match(r'1\s\d{3}\s\d{3}\s\d{4}',num):
            num = '+'+ num
        if re.match(r'\+1\d{10}',num) is not None:
            num = num[:2] + ' ' + num[2:5] + ' ' + num[5:8] + ' ' +num[8:]

    return num

def update_postcode(num):
    return re.search(r'\d{5}',num).group()



OSMFILE = "C:\Users\Zongran\Dropbox\Udacity nano\p4 streetmap data wrangling dataset\san-jose_california_sample.osm"
def test():
    st_types = audit(OSMFILE)
#     assert len(st_types) == 3
    for types in st_types:
        pprint.pprint(dict(types))
        print '\n'
#
    for st_type, ways in st_types[0].iteritems():
        print st_type
        for name in ways:
            better_name = update_postcode(name)
            print name, "=>", better_name
#             assert phone_type_re.match(better_name)
#             if name == "West Lexington St.":
#                 assert better_name == "West Lexington Street"
#             if name == "Baldwin Rd.":
#                 assert better_name == "Baldwin Road"
#
#
if __name__ == '__main__':
    test()
