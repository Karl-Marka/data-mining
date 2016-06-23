import pandas as pd
import numpy as np

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

file = input('Input source data file path: ')
data = pd.read_csv(file, sep='\t', header = None, low_memory = False)
data = pd.DataFrame(data)
data = data.dropna(axis=1,how='all')
dataCropped = pd.DataFrame([])
for i in oligosList:
    for j in data[0]:
        if j == i:
            print(i)
            dt = data.loc[data[0] == i]
            dataCropped = pd.concat([dataCropped, dt])


filename = str(file) + '_cropped.txt'
dataCropped.to_csv(filename, sep = '\t')