#!/usr/bin/python

import pickle
import xgboost as xgb

import numpy as np
import pandas as pd
from sklearn.cross_validation import KFold, train_test_split
from sklearn.metrics import confusion_matrix, mean_squared_error
from sklearn.grid_search import GridSearchCV
from sklearn.datasets import load_iris, load_digits, load_boston
from sklearn.preprocessing import StandardScaler

rng = np.random.RandomState(31337)

train = pd.read_csv('train.txt', header = 0, index_col = 0, sep = '\t')
test = pd.read_csv('test.txt', header = 0, index_col = 0, sep = '\t')
train_labels = pd.read_csv('labels_train.txt', header = None, sep = '\t')

y = train_labels.unstack().tolist() 

header_train = train.columns
index_train = train.index
header_test = test.columns
index_test = test.index

stds = StandardScaler()
stds = stds.fit(train)
train = stds.transform(train)
test = stds.transform(test)

X = pd.DataFrame(data = train, columns = header_train, index = index_train)
test = pd.DataFrame(data = test, columns = header_test, index = index_test)

#kf = KFold(y.shape[0], n_folds=2, shuffle=True, random_state=rng)

xgb_model = xgb.XGBClassifier().fit(X,y)
predictions_train = xgb_model.predict(X)
actuals_train = y
predictions_test = xgb_model.predict(test)
print(confusion_matrix(predictions_train, actuals_train))
print()


xgb_model = xgb.XGBClassifier()
clf = GridSearchCV(xgb_model,
                   {'max_depth': [2,4,6],
                    'n_estimators': [50,100,200]}, verbose=10)
clf.fit(X,y)
print(clf.best_score_)
print(clf.best_params_)
