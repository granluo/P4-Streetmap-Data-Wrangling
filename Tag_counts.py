import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import sys


sys.dont_write_bytecode = True



def count_tags(filename):
        # YOUR CODE HERE
    tagstat = defaultdict(int)

    for event,ele in ET.iterparse(filename):
        tagstat[ele.tag] += 1
    return tagstat
