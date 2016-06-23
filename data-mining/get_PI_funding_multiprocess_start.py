from pandas import read_csv, concat, DataFrame
import multiprocessing
import get_PI_funding_multi

print('Reading database...')
db = read_csv('merged_2014-2016.txt', header=0, sep='\t', iterator=True, chunksize=10000, encoding='cp1252', error_bad_lines=False)
print('Concatenating database...')
db = concat(tp, ignore_index=True)

names1 = read_csv('names1.txt', header = None, sep = '\t', encoding='cp1252')
names1 = names1.unstack()
names2 = read_csv('names2.txt', header = None, sep = '\t', encoding='cp1252')
names2 = names2.unstack()
names3 = read_csv('names3.txt', header = None, sep = '\t', encoding='cp1252')
names3 = names3.unstack()
names4 = read_csv('names4.txt', header = None, sep = '\t', encoding='cp1252')
names4 = names4.unstack()

# Creating a smaller version of the database with only names and cost columns
db = DataFrame([db['PI_NAMEs'], db['TOTAL_COST']])
db = db.T
db = db.dropna(axis=0,how='all')

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=get_PI_funding_multi, args=(DataFrame, db, names1, 1))
    p2 = multiprocessing.Process(target=get_PI_funding_multi, args=(DataFrame, db, names2, 1))
    p3 = multiprocessing.Process(target=get_PI_funding_multi, args=(DataFrame, db, names3, 1))
    p4 = multiprocessing.Process(target=get_PI_funding_multi, args=(DataFrame, db, names4, 1))
    print('Starting thread 1')
    p1.start()
    print('Starting thread 2')
    p2.start()
    print('Starting thread 3')
    p3.start()
    print('Starting thread 4')
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    db = None
    names1 = None
    names2 = None
    names3 = None
    names4 = None