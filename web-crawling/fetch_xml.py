# 'Fetches an XML page from the web, parses it and returns the value between the 'tag' tags'
__version__ = '1.0'
__author__ = 'Karl Marka'

import requests
import xml.etree.ElementTree as ET

def fetch_xml(database, term, tag):
    URL = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=' + str(database) + '&term=' + str(term)
    request = requests.get(URL)
    result = request.content
    root = ET.fromstring(result)
    tag = str(tag)
    count = root.find(tag).text
    return count

print(fetch_xml('pubmed', 'whitfield m', 'Count'))