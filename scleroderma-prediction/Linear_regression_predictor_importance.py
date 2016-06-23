import pandas as pd
import numpy as np
from sklearn import linear_model

file = input('Input training data file path: ')
data = pd.read_csv(file, sep='\t', header = None)
data = pd.DataFrame(data)
names = data.ix[0]
names = names.drop(names.index[0])
names = names.values.tolist()
data = data.dropna(axis=1,how='all')
classifier = data.tail(1)
del classifier[0]
classifier = classifier.unstack()
# deleting first and last rows (names and classifications)
data = data.drop(data.index[0])
data = data.drop(data.index[-1])
oligos = data[0]
oligos = oligos.values.tolist()

file2 = input('Input test data file path: ')
test = pd.read_csv(file2, sep='\t', header = None)
test = pd.DataFrame(test)
test = test.dropna(axis=1,how='all')
test = test.drop(test.index[0])

file3 = input('Input test data classes file path: ')
classes = pd.read_csv(file3, sep='\t', header = None)
classes = pd.DataFrame(classes)
#classes = classes.values.tolist()
#print(classes)
#print(classes.shape)


def closeFunc():
    print('''Type 'quit' and press enter to exit program''')
    answer = input(': ')
    if answer == 'quit':
        quit()
    else:
        closeFunc()

def outputFile(output, file, oligos):
    output = pd.DataFrame(data = output, index = oligos)
    filename = str(file) + '.predictor_importances.txt'
    output.to_csv(filename, sep = "\t")
    print ('Predictor values saved to to file ' + str(filename))
    closeFunc()

def RSS(data, classifier, test, classes, file, names, oligos):
    rssValues = []
    regr = linear_model.LinearRegression()
    for i in range(0, data.shape[0]):
        dt = pd.DataFrame(data.iloc[i])
        dt = dt.drop(dt.index[0])
        rowNr = data.index[i] 
        print('Processing row nr. ' + str(rowNr))      
        regr = regr.fit(dt, classifier)
        testSet = test.ix[rowNr]
        testSet = testSet.drop(testSet.index[0])
        testSet = testSet.values.tolist()
        testSet = pd.DataFrame(data = testSet, index = names)
        predictions = regr.predict(testSet)
        rssScore = np.mean((regr.predict(testSet) - classes) ** 2)
        rssValues.append(rssScore)
    outputFile(rssValues,file,oligos)

RSS(data, classifier, test, classes, file, names, oligos)