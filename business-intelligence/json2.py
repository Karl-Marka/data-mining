# Open URL, retrieve JSON, count the sum of the numbers in the "count" tag
# Python 3.5

import json
import urllib.request

url = 'http://python-data.dr-chuck.net/comments_274490.json'
input = urllib.request.urlopen(url).read()
input = str(input)
input = input.strip('b')
input = input.strip("'")
input = input.replace('\\n', '')


info = json.loads(input)
total = 0

for i in info["comments"]:
    number = int(i["count"])
    total += number
print(total)
    

