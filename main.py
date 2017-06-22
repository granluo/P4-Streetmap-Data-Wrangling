import sys
import Tag_counts
import Tag_type
import Explore_user
import Street_names as st
import pprint

def getfile():
    DATASETLOC = "C:\Users\Zongran\Dropbox\Udacity nano\p4 streetmap data wrangling dataset\san-jose_california_sample.osm"
    return DATASETLOC

def main():
    sys.dont_write_bytecode = True

    dataset = getfile()
    st_types = st.audit(dataset)
    print pprint.pprint(dict(st_types))
    for st_type, ways in st_types.iteritems():
        if st_type in st.get_mapping():
            for name in ways:
                better_name = st.update_name(name, st.get_mapping())
                print name, "=>", better_name
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
