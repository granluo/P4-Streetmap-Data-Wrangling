import re

print re.compile(r'\+1\s\d{3}\s\d{3}\s\d{4}').match("+1 123 123 1232").group()

print re.sub(r'\.','2',' ac  woAai ni 3')

print re.search(r'[A-Z]','dds')


print re.search(r'\d{5}','ca 12345-2134').group()
