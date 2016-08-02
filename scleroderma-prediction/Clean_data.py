import pandas as pd
import numpy as np
import math

print('Removes rows that contain only NaN-s from a tab-separated file')
print('Replaces rest of the Nan-s with row averages')
print('Assumes the last row is labels')
print(' ')
file = input('Path to input data file: ')
data = pd.read_csv(file, sep='\t', header = 0, index_col = 0, low_memory = False)

labels = data.tail(1)
data = data.drop(data.index[-1])
data = data.dropna(axis = 1, how = 'all')

averages = []

print('Calculating averages')
for rowname in data.index:
    row = data.ix[rowname]
    row = row.tolist()
    row = [x for x in row if type(x) != float]
    row = [float(x) for x in row]
    average = np.mean(row)
    averages.append(average)

averages = pd.DataFrame(data = averages, index = data.index)
averages = averages.T

data_new = pd.DataFrame(data = [])

print('Replacing NaN-s')
for rowname in data.index:
    row = data.ix[rowname]
    nafill = float(averages[rowname])
    row = row.fillna(nafill)
    row = row.astype(float)
    data_new = pd.concat([data_new, row], axis = 1)

data_new = data_new.T

data = pd.concat([data_new, labels], axis = 0)



outputfile = str(file) + '_output.txt'
data.to_csv(outputfile, sep = '\t')
print('Results written to: ' + str(outputfile))


def closeFunc():
    print('''Type 'quit' and press enter to exit the program''')
    answer = input(': ')
    if answer == 'quit':
        quit()
    else:
        closeFunc()

closeFunc()