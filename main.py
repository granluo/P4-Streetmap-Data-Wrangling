import sys
import Tag_counts
import Tag_type
import Explore_user
import Street_names as st
import pprint
import xml.etree.cElementTree as ET
import re

def getfile():
    DATASETLOC = "C:\Users\Zongran\Dropbox\Udacity nano\p4 streetmap data wrangling dataset\san-jose_california_sample.osm"
    return DATASETLOC


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

OUTPUTFILE = "sampleoutput.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons","Way","Terrace","Row","Plaza", "Circle", "Loop", "Hill", "Expressway", "Court"]
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd": "Road",
            "Rd.": "Road",
            "Ln": "Lane",
            "court": "Court",
            "Blvd": "Boulevard",
            "Dr": "Drive"
            }
streetname = set()
def main():

    sys.dont_write_bytecode = True

    dataset = getfile()
    # for event, elem in ET.iterparse(dataset, events=("start",)):
    #     if elem.tag == "node" or elem.tag == "way":
    #         for tag in elem.iter("tag"):
    #             if is_street_name(tag):
    #                 m = street_type_re.search(tag.attrib['v']).group()
    #                 if m not in expected:
    #                     streetname.add(tag.attrib['v'])
    # pprint.pprint(streetname)

    st_types = st.audit(OUTPUTFILE)
    print pprint.pprint(dict(st_types))
    for st_type, ways in st_types.iteritems():
        if st_type in st.get_mapping():
            for name in ways:
                better_name = st.update_name(name, st.get_mapping())
                print name, "=>", better_name

    # output osm file
    # with open(OUTPUTFILE, 'w') as output:
    #     output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    #     output.write('<osm>\n  ')
    #
    #     # this is where the output of yield is called on the
    #     for i, element in enumerate(get_element(dataset,mapping, 'v')):
    #         output.write(ET.tostring(element, encoding='utf-8'))
    #
    #     output.write('</osm>')



    # Tagcounts = Tag_counts.count_tags(dataset)
    # pprint.pprint(dict(Tagcounts))
    # keys = Tag_type.process_map(dataset)
    # pprint.pprint(keys)
    # users = Explore_user.users_count(dataset)
    # pprint.pprint(users)

def get_element(osm_file, mapping, attrib_key, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            if elem.tag == 'way' or elem.tag == 'node':
                for tag in elem.iter('tag'):
                    for key in mapping.keys():
                        if re.search(key, ET.tostring(tag)):
                            tag.set(attrib_key, mapping[key])
            yield elem
            root.clear()



def test():


    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            if name == "West Lexington St.":
                assert better_name == "West Lexington Street"
            if name == "Baldwin Rd.":
                assert better_name == "Baldwin Road"



if __name__ == "__main__":
    main()
