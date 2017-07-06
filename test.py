#!/usr/bin/env python
# -*- coding: utf-8 -*-
# content = u'\xe5\xb1\x82\xe5\x8f\xa0\xe6\xa0\xb7\xe5\xbc\x8f\xe8\xa1\xa8'
# print content.encode('latin1').decode('utf8')
# print 'San Jos\xe9'.encode("latin1").decode("utf-8")

# import re
utfbytes = "\xc2\xa9 \xc2\xae \xe2\x84\xa2 \xe9"
print utfbytes, len(utfbytes)
san = u'San Jos\xe9'
print(san == u'San Jos\xe9')
print(isinstance(san,unicode))
print ('San José')
print isinstance('San José',str)

# print (re.search('\xe9',san).group())
# s = "H\u00eatres et \u00e9tang"
#
# print (s.encode("latin1"))
#
# print ("H\u00eatres et \u00e9tang")
# name = san
# name = name.split(',')[0]
# name = name.title()
#
# city_mapping = { "SUnnyvale": "Sunnyvale",
#             u"San Jos\xe9": "San Jose",
#             "Ave": "San Jose",
#             "san jose": "San Jose",
#             "Los Gato": "Los Gatos"
#             }
# print (name in city_mapping)
# u = chr(40960) + 'abcd' + chr(1972)
# print(type('\xe9'))
