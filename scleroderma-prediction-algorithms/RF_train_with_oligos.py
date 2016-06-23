import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

def oligosList():
    oligosPath = input('Path to the file containing the list of oligos to use: ')
    oligos = open(oligosPath)
    oligos = oligos.readlines()
    oligosList = []
    for oligo in oligos:
        item = oligo.strip()
        oligosList.append(item)
    return oligosList

oligosList = oligosList()

file = input('Input training data file path: ')
data = pd.read_csv(file, sep='\t', header = None)
data = pd.DataFrame(data)
data = data.dropna(axis=1,how='all')
classifier = data.tail(1)
del classifier[0]
classifier = classifier.unstack()
dataCropped = pd.DataFrame([])
for i in oligosList:
    for j in data[0]:
        if j == i:
            dt = data.loc[data[0] == i]
            dataCropped = pd.concat([dataCropped, dt])
data = pd.DataFrame.transpose(dataCropped)
# Removing oligo names from dataset
data = data.drop(data.index[0])


estimators = input('How many trees to build?: ')
estimators = int(estimators)

forest = RandomForestClassifier(n_estimators = estimators)
forest = forest.fit(data, classifier)

importances = forest.feature_importances_

importancesList = pd.DataFrame(importances, index=oligosList, columns=['Importance'])
joblib.dump(forest, './model/model.pkl')
    
importancesList.to_csv("importances.txt", sep='\t')

print('Prediction model saved to: /model/model.pkl')
print('Predictor importaces saved as importances.txt')

def closeFunc():
    print('''Type 'quit' and press enter to exit program''')
    answer = input(': ')
    if answer == 'quit':
        quit()
    else:
        closeFunc()

closeFunc()



