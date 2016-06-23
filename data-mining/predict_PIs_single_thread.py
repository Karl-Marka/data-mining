import time
from pandas import read_csv, concat, DataFrame
from time import sleep
import requests
import xml.etree.ElementTree as ET

print('Reading database...')
tp = read_csv('merged2010-2016.txt', header=0, sep='\t', iterator=True, chunksize=10000, encoding='cp1252', error_bad_lines=False)
print('Concatenating database...')
db = concat(tp, ignore_index=True)

print('Creating namelists...')
names = read_csv('PIs.txt', header = None, sep = '\t', encoding='cp1252')
names = names.unstack()

# Creating a smaller version of the database with only names and cost columns
print('Reducing database size...')
db = DataFrame([db['PI_NAMEs'], db['ORG_NAME'], db['ACTIVITY'], db['FY']])
db = db.T
db = db.dropna(axis=0,how='all')

def fetch_count(name, type, journal = ''):
    if journal == '':
        journalVar = ''
    else:
        journalVar = str(journal) + '[journal]'
    name = name.split(',')
    lastName = name[0]
    lastName = lastName.strip()
    firstName = name[1]
    firstName = firstName.strip()
    firstName = firstName[:1]
    name = str(lastName) + ' ' + str(firstName)
    URL = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=' + str(name) + str(type) + '+AND+' + str(journalVar)
    request = requests.get(URL)
    result = request.content
    root = ET.fromstring(result)
    tag = 'Count'
    count = root.find(tag).text
    return count

def writeFile(output):
    filename = 'predictions.txt'
    output.to_csv(filename, sep = '\t')

def stats(name, db = db):    
    #result = dict()
    values = []
    total = fetch_count(name, '[Author]')
    #sleep(1)
    total_last = fetch_count(name, '[Author - Last]')
    #sleep(1)
    nature_first = fetch_count(name, '[Author - First]', "nature")
    #sleep(1)
    nature_last = fetch_count(name, '[Author - Last]', "nature")
    #sleep(1)
    biotech_first = fetch_count(name, '[Author - First]', "nature biotechnology")
    #sleep(1)
    biotech_last = fetch_count(name, '[Author - Last]', "nature biotechnology")
    #sleep(1)
    cell_first = fetch_count(name, '[Author - First]', "cell")
    #sleep(1)
    cell_last = fetch_count(name, '[Author - Last]', "cell")
    #sleep(1)
    nejm_first = fetch_count(name, '[Author - First]', "The New England journal of medicine")
    #sleep(1)
    nejm_last = fetch_count(name, '[Author - Last]', "The New England journal of medicine")
    #sleep(1)
    science_first = fetch_count(name, '[Author - First]', "science")
    #sleep(1)
    science_last = fetch_count(name, '[Author - Last]', "science")
    #sleep(1)
    jama_first = fetch_count(name, '[Author - First]', "Journal of the American Medical Association")
    #sleep(1)
    jama_last = fetch_count(name, '[Author - Last]', "Journal of the American Medical Association")
    #sleep(1)
    noProjects = 0
    year = 2016
    RO1titles = 0
    orgs = set()
    for n,i in enumerate(db['PI_NAMEs']):     
         if name in str(i):
            noProjects += 1
            orgs.add(str(db['ORG_NAME'].iloc[n]))
            if int(db['FY'].iloc[n]) < year:
                year = int(db['FY'].iloc[n])
            if str(db['ACTIVITY'].iloc[n]) == 'R01':
                RO1titles += 1
    orgs = list(orgs)
    highImpact = sum([int(nature_first), int(nature_last), int(biotech_first), int(biotech_last), int(cell_first), int(cell_last), int(nejm_first), int(nejm_last), int(science_first), int(science_last), int(jama_first), int(jama_last)])
    values.append(orgs)
    values.append(year)
    values.append(noProjects)
    values.append(RO1titles)
    values.append(highImpact)
    values.append(total_last)
    values.append(total)
    return values

def predictList(names):
    dataDict = dict()
    turn = len(names) + 1
    for name in names:
        turn -= 1
        print(str(turn) + ' name(s) left to process')
        data = stats(name)
        ratio1 = int(data[5])/int(data[6])
        ratio2 = int(data[4])/int(data[6])
        ratio3 = int(data[3])/int(data[2])
        if 2009 < data[1] < 2013 and ratio1 > 0.33 and ratio2 > 0.2 and ratio3 > 0.33 :
            dataDict.update({name: data})
    results = DataFrame.from_dict(data = dataDict, orient = 'index')
    writeFile(results)

if __name__ == '__main__':
    predictList(names)
