# Scrape HTML and follow n-th link for m times
# Python 3.5

import urllib.request
from bs4 import *

url = input('Enter starting URL: ')
#url = "http://python-data.dr-chuck.net/known_by_Dorian.html"
n = 18
m = 7

def LinksZweiDrei(url, n):
    n = n - 1
    url = str(url)
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html)
    tags = soup('a')
    output = []
    for tag in tags:
        output.append(tag.get('href', None))
    return output[n]

for i in range(0, m):
    #print(url)
    url = LinksZweiDrei(url, n)

print(url)
    