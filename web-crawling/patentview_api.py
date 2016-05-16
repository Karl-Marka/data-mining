# Fetches the number of patents for a given name
__version__ = '1.0'
__author__ = 'Karl Marka'

from requests import get
from html.parser import HTMLParser
from lxml import etree
from json import loads

def fetch_html(lastname, firstname):
    lastname = '"' + str(lastname) + '"'
    firstname = '"' + str(firstname) + '"'
    URL = """http://www.patentsview.org/api/inventors/query?q={"_and":[{"inventor_last_name":""" + lastname + """},{"inventor_first_name":""" + firstname + """}]}&f=["inventor_total_num_patents"]"""
    request = get(URL)
    result = request.content
    result = str(result)
    result = result.strip("b")
    result = result.strip("'")
    parsed = loads(result)
    inventors = parsed["inventors"]
    inventors = inventors[0]
    return inventors["inventor_total_num_patents"]
