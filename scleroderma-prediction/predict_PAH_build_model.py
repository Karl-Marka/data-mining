from pandas import DataFrame, read_csv
from sklearn.cross_validation import train_test_split
from sklearn import linear_model
import numpy as np

data = read_csv('./datasets/train_noduplicate_correl_60.txt', header = 0, index_col = 0, sep = '\t')
data = data.T
labels = read_csv('./datasets/labels_train.txt', header = None, sep = '\t')
labels = labels.unstack().tolist()
#print(X.head(2))
oligos = ['ARL4C','AIF1','S100A11','MYOF','CYBB','LOC93622','LMO2','SLC31A2','FZD1','UPF3A','MS4A4A','SECTM1','C11orf75','DYSF','VRK2']
data = data[oligos]

X_train, X_test, y_train, y_test = train_test_split(data, labels, random_state=5)

clf = linear_model.LogisticRegression(random_state = 5, C = 0.0001, penalty = 'l2')
clf.fit(X_train, y_train)

predictions = clf.predict(X_test)

RSS = np.mean((predictions - y_test)**2)

print('RSS:', RSS)

coefs = clf.coef_.tolist()
coefs = coefs[0]
intercept = clf.intercept_.tolist()

print(coefs)
print(intercept)
oligos.append('Intercept:')
coefs.append(intercept[0])

results = dict(zip(oligos, coefs))

results = DataFrame.from_dict(data = results, orient = 'index')
results.columns = ['Coefficient']
results.to_csv('model_parameters.txt', sep = '\t')
