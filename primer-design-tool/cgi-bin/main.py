#!/usr/bin/python
import cgi
from manager import CodonManager

print 'Content-type: text/html\n'

formdata = cgi.FieldStorage()

peptide = str(formdata.getvalue('peptide'))
asense = int(formdata.getvalue('asense'))
mintemp = int(formdata.getvalue('mintemp'))
maxtemp = int(formdata.getvalue('maxtemp'))

if __name__ == "__main__":

    manager = CodonManager(peptide)
    manager.closest(asense, mintemp, maxtemp)
