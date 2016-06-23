# Parses the XML from a given URL, finds all the numbers contained in the tags specified in the 'path' variable and returns the sum
# Python 3.5

import urllib.request
import xml.etree.ElementTree as ET

url = 'http://python-data.dr-chuck.net/comments_274486.xml'

result = urllib.request.urlopen(url).read()
root = ET.fromstring(result)

path = './/comments//comment//count'
comments = root.findall(path)
sum = 0
for comment in comments:
    comment = int(comment.text)
    sum += comment

print(sum)

