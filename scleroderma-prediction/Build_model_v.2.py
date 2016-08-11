print('Importing libraries')
from pandas import DataFrame, read_csv
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler
import numpy as np

#positive = ['GSM489234', 'GSM489228', 'GSM489221', 'GSM489229', 'GSM489220', 'GSM489223', 'GSM489233', 'GSM489230', 'GSM489231', 'GSM489225', 'GSM489232', 'GSM489205', 'GSM489198', 'GSM489213', 'GSM489202', 'GSM489218', 'GSM489199', 'GSM489208', 'GSM489197', 'GSM489210', 'GSM489212', 'GSM489195', 'GSM489206', 'GSM489217', 'GSM489194', 'GSM489214', 'GSM489203', 'GSM489211']
normprobes = ['A_23_P414913', 'A_24_P237443', 'A_32_P168349', 'A_23_P414654', 'A_24_P192914']

train = read_csv('./datasets_large/train_nocorrelated_top60_normprobes.txt', header = 0, index_col = 0, sep = '\t')
train = train.sort_index(axis = 0)
normprobes_train = train.ix[normprobes]
normprobes_train = normprobes_train.mean(axis = 0)
train = train.subtract(normprobes_train, axis = 1)
train = train.drop(normprobes)
train = train.T
#train_sc = train.ix[positive] 
labels_train_sc = read_csv('./datasets_large/labels_train_sc.txt', sep = '\t', header = None)
labels_train_pah = read_csv('./datasets_large/labels_train_pah.txt', sep = '\t', header = None)
labels_train_sc = labels_train_sc.unstack().tolist()
labels_train_pah = labels_train_pah.unstack().tolist()
header_train = train.columns
index_train = train.index

test = read_csv('./datasets_large/test_nocorrelated_top60_normprobes.txt', header = 0, index_col = 0, sep = '\t')
test = test.sort_index(axis = 0)
normprobes_test = test.ix[normprobes]
normprobes_test = normprobes_test.mean(axis = 0)
test = test.subtract(normprobes_test, axis = 1)
test = test.drop(normprobes)
test = test.T
labels_test_sc = read_csv('./datasets_large/labels_test_sc.txt', sep = '\t', header = None)
labels_test_pah = read_csv('./datasets_large/labels_test_pah.txt', sep = '\t', header = None)
labels_test_sc = labels_test_sc.unstack().tolist()
labels_test_pah = labels_test_pah.unstack().tolist()
header_test = test.columns
index_test = test.index


stds = StandardScaler()
stds = stds.fit(train)
train = stds.transform(train)
train = DataFrame(data = train, columns = header_train, index = index_train)

test = stds.transform(test)
test = DataFrame(data = test, columns = header_test, index = index_test)

means = stds.mean_
std_deviations = stds.std_

means = list(means)
std_deviations = list(std_deviations)

#print(means)
#print(std_deviations)

lr1 = linear_model.LinearRegression()
lr2 = linear_model.LinearRegression()
sc = lr1.fit(train, labels_train_sc)
pah = lr2.fit(train, labels_train_pah)

intercept_sc = sc.intercept_
coefs_sc = sc.coef_

intercept_pah = pah.intercept_
coefs_pah = pah.coef_

print(intercept_sc)
print(list(coefs_sc))
#print(intercept_pah)
#print(list(coefs_pah))

predictions_train_sc = sc.predict(train)
predictions_train_pah = pah.predict(train)
predictions_test_sc = sc.predict(test)
predictions_test_pah = pah.predict(test)

MSE_sc = np.mean((predictions_test_sc - labels_test_sc)**2)
MSE_pah = np.mean((predictions_test_pah - labels_test_pah)**2)

#print('MSE on Sc:', MSE_sc)
#print('MSE on PAH:', MSE_pah)

#print(list(predictions_train_sc))
#print(list(predictions_train_pah))

#print(list(predictions_test_sc))
#print(list(predictions_test_pah))