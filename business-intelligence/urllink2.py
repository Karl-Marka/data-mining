# Scrape HTML 
# Python 3.5
import urllib.request
from bs4 import *

url = input('Enter URL ')
#url = 'http://python-data.dr-chuck.net/comments_274489.html'
tagname = input('Tag tag ')
html = urllib.request.urlopen(url).read()

soup = BeautifulSoup(html)

tags = soup(tagname)
contentsList = []
for tag in tags:
    # Look at the parts of a tag
    #print 'URL:',tag.get('href', None)
    print ('Contents: ' + str(tag.contents))
    contentsList.append(tag.contents)

sum = 0
for item in contentsList:
    item = int(item[0])
    sum += item

print(sum)