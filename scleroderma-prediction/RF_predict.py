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


file = input('Input prediction data file path: ')
data = pd.read_csv(file, sep='\t', header = None)
data = pd.DataFrame(data)
data = data.dropna(axis=1,how='all')
names = data.ix[0]
del names[0]
names = names.tolist()

dataCropped = pd.DataFrame([])
for i in oligosList():
    for j in data[0]:
        if j == i:
            dt = data.loc[data[0] == i]
            dataCropped = pd.concat([dataCropped, dt])

data = pd.DataFrame.transpose(dataCropped)
# Removing oligo names from dataset
data = data.drop(data.index[0])


filename = input('Enter path to the RF model file (default: ./model/model.pkl): ')

def predict(filename):
    forest = joblib.load(filename) 
    output = forest.predict(data)
    output = pd.DataFrame(output, index = names, columns = ['Type'])
    print(output)
    output.to_csv('predictions.txt', sep = "\t")
    print ('Predictions saved to file predictions.txt')
    closeFunc()

def select(filename):
    if len(filename)==0:
        filename = './model/model.pkl'
        predict(filename)
    else: 
        predict(filename)

def closeFunc():
    print('''Type 'quit' and press enter to exit program''')
    answer = input(': ')
    if answer == 'quit':
        quit()
    else:
        closeFunc()

select(filename)
