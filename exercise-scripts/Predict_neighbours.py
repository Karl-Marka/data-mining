import pandas as pd
from sklearn.svm import SVC
from sklearn import neighbors
import numpy as np
from sklearn.preprocessing import StandardScaler

train = pd.read_csv('train_merged.txt', header = 0, index_col = 0, sep = '\t')
train_labels = pd.read_csv('labels_merged.txt', header = None, sep = '\t')
test = pd.read_csv('skoorimiseks.txt', header = 0, index_col = 0, sep = '\t')
#test_labels = pd.read_csv('labels_test.txt', header = None, sep = '\t')

train_labels = train_labels.unstack().tolist()
#test_labels = test_labels.unstack().tolist()

header_train = train.columns
index_train = train.index
header_test = test.columns
index_test = test.index

stds = StandardScaler()
stds = stds.fit(train)
train = stds.transform(train)
test = stds.transform(test)

train = pd.DataFrame(data = train, columns = header_train, index = index_train)
test = pd.DataFrame(data = test, columns = header_test, index = index_test)

#print(train_labels)
#print(train)

lr = neighbors.KNeighborsClassifier(algorithm = 'ball_tree', n_neighbors = 10, weights='uniform', leaf_size = 15, n_jobs = -1)
lr = lr.fit(train, train_labels)

predictions = lr.predict(train)
predictions = list(predictions)
predictions_test = lr.predict(test)
predictions_test = list(predictions_test)

#print(predictions)

operand = [(a - b)**2 for a, b in zip(predictions, train_labels)]
MSE = np.mean(operand)

#operand_t = [(a - b)**2 for a, b in zip(predictions_test, test_labels)]
#MSE_t = np.mean(operand_t)

print('In-sample MSE:',MSE)
#print('Out of sample MSE:',MSE_t)


f = open('predictions_scoring_neighbours.txt', 'w')
for i in predictions_test:
  f.write("%s\n" % i)
f.close()
