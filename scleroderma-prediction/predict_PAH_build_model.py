from pandas import DataFrame, read_csv
from sklearn.cross_validation import train_test_split
from sklearn import linear_model
import numpy as np

data = read_csv('x.txt', header = 0, index_col = 0, sep = '\t')
data = data.T
labels = read_csv('y.txt', header = None, sep = '\t')
labels = labels.unstack().tolist()
#print(X.head(2))
oligos = ['A_32_P30710', 'A_24_P148094', 'A_23_P77455', 'A_23_P148255', 'A_23_P141044', 'A_32_P103131', 'A_23_P121596', 'A_23_P24948', 'A_23_P68121', 'A_24_P396994']
data = data[oligos]

X_train, X_test, y_train, y_test = train_test_split(data, labels, random_state=5)

clf = linear_model.LogisticRegression(random_state = 2)
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
