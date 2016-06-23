import multiprocessing
import time
from pandas import read_csv, concat, DataFrame
import requests
import xml.etree.ElementTree as ET
from queue import Queue

print('Creating namelists...')
names = read_csv('PIs.txt', header = None, sep = '\t', encoding='cp1252')
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
    #names = [names1, names2, names3, names4, names5, names6, names7, names8]
    #for i in names:
     #   yield i


print('Creating database...')
tp = read_csv('merged.txt', header=0, sep='\t', iterator=True, chunksize=10000, encoding='cp1252', error_bad_lines=False)
db = concat(tp, ignore_index=True)
db = DataFrame([db['PI_NAMEs'], db['ORG_NAME'], db['ACTIVITY'], db['FY']])
db = db.T
db = db.dropna(axis=0,how='all')


def dump_queue(queue):
    print('Starting dump...')
    results = dict()
    for i in queue.get():
        results.update(i)   
    #print(results)
    filename = 'predictions.txt'
    output = DataFrame.from_dict(data = results, orient = 'index')
    output.columns = ['Institution(s)', 'First Grant', 'Total Grants', 'R01 Grants', 'High-Impact Publications', 'First Author', 'Last Author', 'Total', 'Score']
    print('Writing output file...')
    output.to_csv(filename, sep = '\t')

def fetch_count(name, type, journal = ''):
    try:
        if journal == '':
            journalVar = ''
        else:
            journalVar = str(journal) + '[journal]'
        #print('Processing name: ' + name)
        URL = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=' + str(name) + str(type) + '+AND+' + str(journalVar) + '&tool=ncbi_api&email=karl.marka@ttu.ee'
        request = requests.get(URL)
        result = request.content
        root = ET.fromstring(result)
        tag = 'Count'
        count = root.find(tag).text
        return count
    except:
        return 0


def filter(db, names, threadNO):
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
        #if 2005 < year < 2012:
        if 2000 < year < 2007:
            filtered.add(name)
    filtered = list(filtered)
    return filtered

def stats(name, db):   
    #result = dict()
    values = []
    name = name.split(',')
    lastName = name[0]
    lastName = lastName.strip()
    if len(name) > 1:
        firstName = name[1]
        firstName = firstName.strip()
        firstName = firstName.split(' ')
        firstName1 = firstName[0]
        firstName1 = firstName1.strip()
        firstName1 = firstName1.strip('.')
        firstNameLetter = firstName1[:1]
    else:
        firstName = 'None'
        firstName1 = 'None'
        firstName2 = 'None'
        firstNameLetter = 'N'
    if len(firstName) > 1 :
        firstName2 = firstName[1]
        firstName2 = firstName2.strip()
        firstName2 = firstName2.strip('.')
        firstName2 = firstName2[:1]
        name_full = str(lastName) + ', ' + str(firstName1) + ' ' + str(firstName2)
        name_letters = str(lastName) + ' ' + str(firstNameLetter) + str(firstName2)
    else:
        name_full = str(lastName) + ', ' + str(firstName1)
        name_letters = str(lastName) + ' ' + str(firstNameLetter)
    total = fetch_count(name_letters, '[Author]')
    #sleep(1)
    total_last = fetch_count(name_letters, '[Author - Last]')
    total_first = fetch_count(name_letters, '[Author - First]')
    #sleep(1)
    nature_first = fetch_count(name_letters, '[Author - First]', "nature")
    #sleep(1)
    nature_last = fetch_count(name_letters, '[Author - Last]', "nature")
    #sleep(1)
    biotech_first = fetch_count(name_letters, '[Author - First]', "nature biotechnology")
    #sleep(1)
    biotech_last = fetch_count(name_letters, '[Author - Last]', "nature biotechnology")
    #sleep(1)
    cell_first = fetch_count(name_letters, '[Author - First]', "cell")
    #sleep(1)
    cell_last = fetch_count(name_letters, '[Author - Last]', "cell")
    #sleep(1)
    nejm_first = fetch_count(name_letters, '[Author - First]', "The New England journal of medicine")
    #sleep(1)
    nejm_last = fetch_count(name_letters, '[Author - Last]', "The New England journal of medicine")
    #sleep(1)
    science_first = fetch_count(name_letters, '[Author - First]', "science")
    #sleep(1)
    science_last = fetch_count(name_letters, '[Author - Last]', "science")
    #sleep(1)
    jama_first = fetch_count(name_letters, '[Author - First]', "Journal of the American Medical Association")
    #sleep(1)
    jama_last = fetch_count(name_letters, '[Author - Last]', "Journal of the American Medical Association")
    noProjects = 0
    RO1titles = 0
    noProjects = 0
    year = 2016
    orgs = set()
    for n,i in enumerate(db['PI_NAMEs']):     
         if name_full in str(i):
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
    values.append(total_first)
    values.append(total_last)
    values.append(total)
    return values


def predictList(db, names, threadNO):
    names = filter(db, names, threadNO)
    print('Started processing names in thread no. ' + str(threadNO))
    print(str(len(names)) + ' names in total in thread no. ' + str(threadNO))
    outDict = dict()
    turn = len(names) + 1
    for name in names:
        turn -= 1
        print('Thread ' +  str(threadNO) + ' ' + str(turn) + ' name(s) left to process.')
        data = stats(name, db)
        orgs = str(data[0])
        year = int(data[1])
        noProjects = int(data[2])
        R01titles = int(data[3])
        highImpact = int(data[4])
        total_first = int(data[5])
        total_last = int(data[6])
        total = int(data[7])
        years = 2017 - year
        if 0 < total < 300 and R01titles != 0 and total_last != 0 and noProjects != 0 and years != 0 :
            R01_Year = R01titles/years
            HI_Year = highImpact/years
            HI_Total = highImpact/total
            Last_Total = total_last/total
            R01_Total = R01titles/noProjects
            Pub_Year = total/years
            First_Last = total_first/total_last
            First_Total = total_first/total
            score = 27 * R01_Year + 25 * HI_Year + 22 * HI_Total + 14 * Last_Total + 6 * R01_Total + 4 * Pub_Year + 2 * First_Last + First_Total
            if score >= 100:
                outDict.update({name: [orgs, year, noProjects, R01titles, highImpact, total_first, total_last, total, score]}) 
    #q.put(outDict)
    return outDict
    #writeFile(outDict, threadNO)
    print('Thread ' + str(threadNO) + ' finished.')
    #results = DataFrame.from_dict(data = dataDict, orient = 'index')
    #writeFile(results, threadNo)


if __name__ == '__main__':    
    q = multiprocessing.Queue()
    print('Starting threads')
    with multiprocessing.Pool(8) as p:
        q.put((p.starmap(predictList, [(db, names1, 1), (db, names2, 2), (db, names3, 3), (db, names4, 4), (db, names5, 5), (db, names6, 6), (db, names7, 7), (db, names8, 8)])))
    db = None    
    dump_queue(q)



