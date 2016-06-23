from pandas import DataFrame, read_csv
from sklearn.cross_validation import train_test_split
from sklearn import linear_model
import numpy as np

data = read_csv('Illumina_normalized_scaled.txt', header = 0, index_col = 0, sep = '\t')
data = data.T
labels = read_csv('labels_illumina.txt', header = None, sep = '\t')
labels = labels.unstack().tolist()
#print(X.head(2))
oligos = ['ILMN_2154115', 'ILMN_1755115', 'ILMN_1661537', 'ILMN_1711516', 'ILMN_1767281', 'ILMN_1779813', 'ILMN_1699100', 'ILMN_1715393', 'ILMN_1789387', 'ILMN_1812877']
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
results.to_csv('model_parameters_illumina.txt', sep = '\t')
