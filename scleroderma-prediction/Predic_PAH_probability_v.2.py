print('Importing libraries')
from pandas import DataFrame, read_csv
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler


print('Reading and normalizing data')
train = read_csv('./datasets_PAH/train_top10pc.txt', header = 0, index_col = 0, sep = '\t')
train = train.T
header = train.columns
index = train.index
stds = StandardScaler()
stds = stds.fit(train)
train = stds.transform(train)
train = DataFrame(data = train, columns = header, index = index)
test = read_csv('./datasets_PAH/test_top10pc.txt', header = 0, index_col = 0, sep = '\t')
gene_exp = test.copy()
test = test.T
header_test = test.columns
index_test = test.index
#stds = StandardScaler()
test = stds.transform(test)
test = DataFrame(data = test, columns = header_test, index = index_test)
labels = read_csv('./datasets_PAH/labels_train.txt', sep = '\t', header = None)
labels = labels.unstack().tolist()
labels_test = read_csv('./datasets_PAH/labels_test.txt', sep = '\t', header = None)
labels_test = labels_test.unstack().tolist()
#gene_data = read_csv('./datasets/gene_data.txt', header = 0, index_col = 0, sep = '\t')

lr = linear_model.LinearRegression()
lr = lr.fit(train, labels)

predictions = lr.predict(test)
predictions = list(predictions)
predictions_train = lr.predict(train)
predictions_train = list(predictions_train)

print('Train set:',predictions_train,'Real labels:',labels)
print('Test set:',predictions,'Real labels:',labels_test)

#predictions = dict(zip(index_test, predictions))

#up = dict()
#down = dict()


'''
for i in gene_data.index:
    condition = gene_data.loc[i,'condition']
    value = gene_data.loc[i,'value']
    if condition == 'UP':
        up.update({i : value})
    elif condition == 'DOWN':
        down.update({i : value})

for patient in gene_exp.columns:
    score = 0
    data = gene_exp[patient]
    for gene in data.index:
        if gene in up.keys():
            if data.ix[gene] > up.get(gene):
                score += 1
        elif gene in down.keys():
            if data.ix[gene] < down.get(gene):
                    score += 1
    probability = int(round((score/65)*100,0))
    if predictions.get(patient) >= 0.5:
        if probability < 50:
           print('Patient',patient,'is Scleroderma negative') 
        if 70 > probability >= 50 :
            print('Patient',patient,'is borderline with a gene exp. similiarity of',probability,'% to a reference Scleroderma gene exp. pattern')
        elif probability >= 70 :
            print('Patient',patient,'is Scleroderma positive with a gene exp. similiarity of',probability,'% to a reference Scleroderma gene exp. pattern')              
    elif predictions.get(patient) < 0.5 :
        print('Patient',patient,'is Scleroderma negative')
        
'''



