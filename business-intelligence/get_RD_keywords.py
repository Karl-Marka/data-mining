from pandas import DataFrame, read_csv, concat

print('Creating database...')
tp = read_csv('merged2014-2016.txt', header=0, sep='\t', iterator=True, chunksize=10000, encoding='cp1252', error_bad_lines=False)
db = concat(tp, ignore_index=True)
db = DataFrame([db['NIH_SPENDING_CATS'], db['ORG_DEPT'], db['PROJECT_TERMS'], db['PROJECT_TITLE'], db['STUDY_SECTION_NAME'], db['TOTAL_COST']])
db = db.T
db = db.dropna(axis=0,how='all')

uniqueterms = set()

project_terms = db['PROJECT_TERMS']
project_terms = project_terms.dropna(how='all')

for row in project_terms:
    terms = row.split(';')
    for term in terms:
        item = term.strip()
        if len(item) > 2:
            uniqueterms.add(item)

project_terms = None

uniqueterms = list(uniqueterms)
uniqueterms2 = []

for i in uniqueterms:
    term2 = i.strip()
    uniqueterms2.append(term2)

print(len(uniqueterms2),'unique terms found')


result = DataFrame(data = uniqueterms2)
result.to_csv('RD_keywords.txt', sep = '\t') 
    
