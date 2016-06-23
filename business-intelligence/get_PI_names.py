from pandas import read_csv, concat, DataFrame

print('Reading database...')
tp = read_csv('merged_2014-2016.txt', header=0, sep='\t', iterator=True, chunksize=10000, encoding='cp1252', error_bad_lines=False)
print('Concatenating database...')
db = concat(tp, ignore_index=True)

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
# Cleaning the database from memory
db = None

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
for x in unique:
    x = str(x)
    uniqueNames.add(x)

uniqueNames = list(uniqueNames)


print("Total of " + str(len(uniqueNames)) + " unique PI-s found in the database")


uniqueNames = DataFrame(data = uniqueNames, index = None, columns = ['Name'])
uniqueNames.to_csv("PIs.txt", sep = '\t')
