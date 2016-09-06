import pandas as pd
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler

train = pd.read_csv('train.txt', header = 0, index_col = 0, sep = '\t')
train_labels = pd.read_csv('labels_train.txt', header = None, sep = '\t')
#test = pd.read_csv('test.txt', header = 0, index_col = 0, sep = '\t')
#test_labels = pd.read_csv('labels_test.txt', header = None, sep = '\t')

train_labels = train_labels.unstack().tolist()

header_train = train.columns
index_train = train.index
#header_test = test.columns
#index_test = test.index

stds = StandardScaler()
stds = stds.fit(train)
train = stds.transform(train)
#test = stds.transform(test)

train = pd.DataFrame(data = train, columns = header_train, index = index_train)
#test = pd.DataFrame(data = test, columns = header_test, index = index_test)

print(train_labels)
#print(train)


lr = linear_model.LinearRegression()
lr = lr.fit(train, train_labels)

predictions = lr.predict(train)
predictions = list(predictions)

print(predictions)


f = open('predictions_train.txt', 'w')
for i in predictions:
  f.write("%s\n" % i)
f.close()

print('Finished execution')

