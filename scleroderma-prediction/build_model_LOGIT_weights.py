from pandas import DataFrame, read_csv, concat
from sklearn.cross_validation import train_test_split
from sklearn import linear_model
import numpy as np

data = read_csv('./datasets/train_noduplicate.txt', header = 0, index_col = 0, sep = '\t')
if 'Rank' in data.columns:
    del data['Rank']
    print('Deleted Ranks')
data = data.T
labels = read_csv('./datasets/labels_train.txt', header = None, sep = '\t')
labels = labels.unstack().tolist()
weights = read_csv('./datasets/LDA_weights.txt', header = 0, sep = '\t')
weights_list = weights['weight'].tolist()
ids = weights['id'].tolist()
test = read_csv('./datasets/test_noduplicate.txt', header = 0, index_col = 0, sep = '\t')
if 'Rank' in test.columns:
    del test['Rank']
    print('Deleted Ranks')
test = test.T
labels_test = read_csv('./datasets/labels_test.txt', header = None, sep = '\t')
labels_test = labels_test.unstack().tolist()
#print(X.head(2))

weights = dict(zip(ids, weights_list))
#print(weights)

def transform(data):
    data_tf = DataFrame(data = [])
    for column in data:
        weight = weights[column]
        probevalues = data[column].tolist()
        newvalues = []
        for row in probevalues:
            value = row * weights[column]
            newvalues.append(value)
        data_tf[str(column)] = newvalues
    data_tf.index = data.index
    #data_tf.to_csv('data_tf.txt', sep = '\t')
    return data_tf

train = transform(data)
test = transform(test)

clf = linear_model.LogisticRegression(random_state = 5, C = 0.0001, penalty = 'l2')
clf.fit(train, labels)

predictions = clf.predict(test)
MSE = np.mean((predictions - labels_test)**2)

print('Predicted labels:',predictions)
print('True labels:',labels_test)
print('MSE:', MSE)

coefs = clf.coef_.tolist()
coefs = coefs[0]
intercept = clf.intercept_.tolist()

#print(coefs)
#print(intercept)
oligos = data.columns
oligos = oligos.tolist()
oligos.append('Intercept:')
coefs.append(intercept[0])

results = dict(zip(oligos, coefs))

results = DataFrame.from_dict(data = results, orient = 'index')
results.columns = ['Coefficient']
results.to_csv('model_parameters_weights.txt', sep = '\t')

