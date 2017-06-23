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

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons","Way","Terrace","Row","Plaza", "Circle", "Loop", "Hill", "Expressway", "Court"]

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

    st_types = st.audit(dataset)
    print pprint.pprint(dict(st_types))
    # for st_type, ways in st_types.iteritems():
    #     if st_type in st.get_mapping():
    #         for name in ways:
    #             better_name = st.update_name(name, st.get_mapping())
    #             print name, "=>", better_name
    # Tagcounts = Tag_counts.count_tags(dataset)
    # pprint.pprint(dict(Tagcounts))
    # keys = Tag_type.process_map(dataset)
    # pprint.pprint(keys)
    # users = Explore_user.users_count(dataset)
    # pprint.pprint(users)


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
