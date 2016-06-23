import multiprocessing
import time
from pandas import read_csv, concat, DataFrame
import requests
import xml.etree.ElementTree as ET
from queue import Queue

print('Creating database...')
tp = read_csv('merged2014-2016.txt', header=0, sep='\t', iterator=True, chunksize=10000, encoding='cp1252', error_bad_lines=False)
db = concat(tp, ignore_index=True)
db = DataFrame([db['NIH_SPENDING_CATS'], db['ORG_DEPT'], db['PROJECT_TERMS'], db['PROJECT_TITLE'], db['STUDY_SECTION_NAME'], db['TOTAL_COST']])
db = db.T
db = db.dropna(axis=0,how='all')



print('Creating keyword lists')
names = read_csv('RD_keywords.txt', header = None, sep = '\t', encoding='cp1252')
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


def dump_queue(queue):
    print('Starting dump...')
    results = dict()
    for i in queue.get():
        results.update(i)   
    #print(results)
    filename = 'RD_keywords_stats.txt'
    output = DataFrame.from_dict(data = results, orient = 'index')
    output.columns = ['Grants', 'Total Funding']
    print('Writing output file...')
    output.to_csv(filename, sep = '\t')



def main(db, names, threadNO):
    print('Starting thread',threadNO)
    funding = dict()
    turn = 0
    for term in names:
        try:
            print('Thread',threadNO,'Processing:',term,len(names)-turn,'terms left to process')
            turn += 1    
            funding_sum = 0
            number = 0
            data = []         
            for n,i in enumerate(db['PROJECT_TERMS']):
                if type(i) != float and term in i :
                    number += 1
                    grant_sum = int(db['TOTAL_COST'].iloc[n])
                    funding_sum += grant_sum
            data.append(number)
            data.append(funding_sum)
            print(term,data)
            funding.update({term:data})
        except:
            pass
    return funding


if __name__ == '__main__':    
    q = multiprocessing.Queue()
    print('Starting threads')
    with multiprocessing.Pool(8) as p:
        q.put((p.starmap(main, [(db, names1, 1), (db, names2, 2), (db, names3, 3), (db, names4, 4), (db, names5, 5), (db, names6, 6), (db, names7, 7), (db, names8, 8)])))
    db = None    
    dump_queue(q) 
    
