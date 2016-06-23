import multiprocessing
import time
from pandas import read_csv, concat, DataFrame
from time import sleep
import requests
import xml.etree.ElementTree as ET
from queue import Queue

print('Creating database...')

tp = read_csv('merged2010-2016.txt', header=0, sep='\t', iterator=True, chunksize=10000, encoding='cp1252', error_bad_lines=False)
db = concat(tp, ignore_index=True)
db = DataFrame([db['PI_NAMEs'], db['ORG_NAME'], db['ACTIVITY'], db['FY']])
db = db.T
db = db.dropna(axis=0,how='all')

#print('Creating namelists...')
names = read_csv('800_names.txt', header = None, sep = '\t', encoding='cp1252')
names = names.unstack()

# Splitting names into eight parts
first = round(len(names)/8)
second = 2 * first
third = 3 * first
fourth = 4 * first
fifth = 5 * first
sixth = 6 * first
seventh = 7 * first
names1 = names[:first]
names2 = names[first:second]
names3 = names[second:third]
names4 = names[third:fourth]
names5 = names[fourth:fifth]
names6 = names[fifth:sixth]
names7 = names[sixth:seventh]
names8 = names[seventh:]
names = None

out = multiprocessing.Queue()

def dump_queue(queue):
    print('Starting dump...')
    """
    Empties all pending items in a queue and returns them in a list.
    """
    result = dict()

    for i in iter(queue.get):
        result.update(i)
    sleep(.1)
    print('Writing output file...')
    filename = 'predictions.txt'
    print(len(result))
    output = DataFrame(data = result)
    output.to_csv(filename, sep = '\t')

def fetch_count(name, type, journal = ''):
    try:
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
    except:
        return 0

def writeFile(output, threadNO):
    print('Writing output file...')
    filename = 'predictions_' + str(threadNO) + '.txt'
    output = DataFrame.from_dict(data = output, orient = 'index')
    output.to_csv(filename, sep = '\t')

def filter(names, threadNO, db = db):
    print('Started thread no. ' + str(threadNO))
    print('Thread ' + str(threadNO) + ' prefiltering names.')
    turn = len(names) + 1
    filtered = set()
    for name in names:
        turn -= 1
        print('Thread ' +  str(threadNO) + ' ' + str(turn) + ' name(s) left to prefilter.')    
        year = 2016
        for n,i in enumerate(db['PI_NAMEs']):
            if name in str(i):
                if int(db['FY'].iloc[n]) < year:
                    year = int(db['FY'].iloc[n])
        if 2009 < year < 2013:
            filtered.add(name)
    filtered = list(filtered)
    predictList(filtered, threadNO)

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
    RO1titles = 0
    orgs = set()
    for n,i in enumerate(db['PI_NAMEs']):     
         if name in str(i):
            noProjects += 1
            orgs.add(str(db['ORG_NAME'].iloc[n]))
            if str(db['ACTIVITY'].iloc[n]) == 'R01':
                RO1titles += 1
    orgs = list(orgs)
    highImpact = sum([int(nature_first), int(nature_last), int(biotech_first), int(biotech_last), int(cell_first), int(cell_last), int(nejm_first), int(nejm_last), int(science_first), int(science_last), int(jama_first), int(jama_last)])
    values.append(orgs)
    #values.append(year)
    values.append(noProjects)
    values.append(RO1titles)
    values.append(highImpact)
    values.append(total_last)
    values.append(total)
    return values


def predictList(names, threadNO, out = out):
    print('Started processing names in thread no. ' + str(threadNO))
    print(str(len(names)) + ' names in total in thread no. ' + str(threadNO))
    outDict = dict()
    turn = len(names) + 1
    for name in names:
        turn -= 1
        print('Thread ' +  str(threadNO) + ' ' + str(turn) + ' name(s) left to process.')
        data = stats(name)
        total = int(data[5])
        if total != 0 :
            ratio1 = int(data[4])/total        
            ratio2 = int(data[3])/total
            ratio3 = int(data[2])/int(data[1])
            if ratio1 > 0.25 and ratio2 > 0.15 and ratio3 > 0.25 :
                outDict.update({name: data[0]})
    return outDict
    #writeFile(outDict, threadNO)
    print('Thread ' + str(threadNO) + ' finished.')
    #results = DataFrame.from_dict(data = dataDict, orient = 'index')
    #writeFile(results, threadNo)

if __name__ == '__main__':
    q = Queue()
    worker_1 = multiprocessing.Process(target=q.put, args=(filter(names1, 1),))
    worker_2 = multiprocessing.Process(target=q.put, args=(filter(names2, 2),))
    worker_3 = multiprocessing.Process(target=q.put, args=(filter(names3, 3),))
    worker_4 = multiprocessing.Process(target=q.put, args=(filter(names4, 4),))
    worker_5 = multiprocessing.Process(target=q.put, args=(filter(names5, 5),))
    worker_6 = multiprocessing.Process(target=q.put, args=(filter(names6, 6),))
    worker_7 = multiprocessing.Process(target=q.put, args=(filter(names7, 7),))
    worker_8 = multiprocessing.Process(target=q.put, args=(filter(names8, 8),))
    print('Starting threads')
    worker_1.start()
    worker_2.start()
    worker_3.start()
    worker_4.start()
    worker_5.start()
    worker_6.start()
    worker_7.start()
    worker_8.start()
    db = None
    worker_1.join()
    worker_2.join()
    worker_3.join()
    worker_4.join()
    worker_5.join()
    worker_6.join()
    worker_7.join()
    worker_8.join()
    #out.put('STOP')
    dump_queue(q)





