from pandas import read_csv, concat, DataFrame, isnull
import requests
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np

startyear = 2008
endyear = 2017
type = 'R43'

print('Reading database...')
tp = read_csv('merged2008-2016.txt', header=0, sep='\t', iterator=True, chunksize=10000, encoding='cp1252', error_bad_lines=False)
print('Concatenating database...')
db = concat(tp, ignore_index=True)
db_full = db.copy()

db = db[['ACTIVITY', 'PI_NAMEs']]
db = db.dropna()
db = db[db['ACTIVITY'].str.contains(type)]

print("Number of grant entries in the database: " + str(len(db)))


namesInDb = db['PI_NAMEs']
namesInDb = namesInDb.tolist()

print("Finding unique research teams from the database...")
unique = set()
for x in namesInDb:
    x = str(x)
    unique.add(x)

unique = list(unique)
unique = [x for x in unique if x != 'nan']

print("Finding unique PI's...")
uniqueNames = set()
for i in unique:
    i = str(i)
    i = i.strip(';')
    i = i.strip('(contact)')
    i = i.replace(',','/')
    PIs = i.split(';')
    for j in PIs:
        j = j.strip()
        j = j.strip('(contact)')
        j = j.strip('.')
        if j.count('/') == 1:
            if len(j) > 5:
                j = j.replace('/',',')
                uniqueNames.add(j)
            else:
                pass
        elif j.count('/') > 1:
            j = j.replace('/',',',1)
            PIsD = j.split('/')
            name = PIsD[0]
            if len(name) > 5:
                uniqueNames.add(name)



# Freeing up some memory
unique = None
unique = list(uniqueNames)
uniqueNames = None
uniqueNames = set()
print("Double-checking names...")
uniqueNames2 = set()
uniqueNames3 = set()

for y in unique:
    y = str(y)
    y = y.strip()
    y = y.strip('.')
    if y.count('.') > 0:
        y = y.split('.')
        uniqueNames2.add(y[0])
    else:
        uniqueNames2.add(y)

uniqueNames = None

for a in uniqueNames2:
    a = str(a)
    a = a.strip()
    a = a.strip('.')
    a = a.strip()
    a = a.split(' ')
    if len(a) == 2 :
        if len(a[0]) > 1 and len(a[1]) > 1:
            PI = str(a[0]) + ' ' + str(a[1])
            uniqueNames3.add(PI)
    if len(a) == 3 :
        if len(a[0]) > 1 and len(a[1]) > 1 and len(a[2]) > 1:
            PI = str(a[0]) + ' ' + str(a[1]) + ' ' + str(a[2])
            uniqueNames3.add(PI)
    if len(a) == 4 :            
        if len(a[0]) > 1 and len(a[1]) > 1 and len(a[2]) > 1 and len(a[3]) > 1:
            PI = str(a[0]) + ' ' + str(a[1]) + ' ' + str(a[2]) + ' ' + str(a[3])
            uniqueNames3.add(PI)


uniqueNames2 = None
uniqueNames = list(uniqueNames3)


print("Total of " + str(len(uniqueNames)) + " unique PI-s found in the database")



def getPublications(name, startyear, endyear):
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
        name_letters = str(lastName) + ' ' + str(firstNameLetter) + str(firstName2)
    else:
        name_letters = str(lastName) + ' ' + str(firstNameLetter)
    try:
        URL = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=' + str(name_letters) + '[Author]+AND+("' + str(startyear) + '/01/01"[PDAT] : "' + str(endyear) + '/01/01"[PDAT])&tool=ncbi_api&email=karl.marka@ttu.ee'
        request = requests.get(URL)
        result = request.content
        root = ET.fromstring(result)
        tag = 'Count'
        count = root.find(tag).text
        return count
    except:
        return 0


#R43
print('Processing grants')


count = len(uniqueNames)
data = dict()

for name in uniqueNames:
    values = []
    publications = getPublications(name, startyear, endyear)
    total_funding = 0
    for n,i in enumerate(db_full['PI_NAMEs']):     
        if name in str(i):
            if isnull(db_full['TOTAL_COST'].iloc[n]) == False :
                funding = int(db_full['TOTAL_COST'].iloc[n])
                total_funding += funding
    if int(publications) < 40 :
        values.append(publications)
        values.append(total_funding)
        data.update({name:values})
    count -= 1
    print(count, 'names left to process')

data = DataFrame.from_dict(data, orient = 'index', dtype = int)

correl = np.corrcoef(data, rowvar = 0)
correl = correl[0,1]
print('Pearson product-moment correlation coefficient: ', correl)

print('Creating the plot')
fig = plt.figure(figsize=(20,10)) 
plt.xlim(0, 40) 
#plt.ylim(0, 5000000)     
plt.xlabel("No of publications")
plt.ylabel("Amount of funding")
plt.title("Relationship between the no. of publications and funding between the years " + str(startyear) + " - 2016")
plt.scatter(data[0], data[1])
content = 'Pearson product-moment correlation coefficient: ' + str(correl)
plt.figtext(.05, .05, content)
fig.savefig('plot1.png')            



