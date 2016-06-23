from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
import pandas as pd

def oligosList():
    oligosPath = input('Path to the file containing the list of oligos to use: ')
    oligos = open(oligosPath)
    oligos = oligos.readlines()
    oligosList = []
    for oligo in oligos:
        item = oligo.strip()
        oligosList.append(item)
    return oligosList


def closeFunc():
    print('''Type 'quit' and press enter to exit program''')
    answer = input(': ')
    if answer == 'quit':
        quit()
    else:
        closeFunc()

def outputFile(output, file, oligos):
    #output = pd.DataFrame(data = output, index = None, columns = oligos)
    output = output.T
    filename = str(file) + '.f_classif.txt'
    output.to_csv(filename, sep = "\t")
    print ('Predictor values saved to to file ' + str(filename))
    closeFunc()

def main(file, oligosList):     
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
    #Removing oligo names from dataset
    data = data.drop(data.index[0])
    #For selecting a number of best features:
    #result = SelectKBest(f_classif, k="all").fit_transform(data, classifier)
    result = f_classif(data, classifier)
    Fval = result[0]
    Pval = result[1]
    result = pd.DataFrame(data = [Fval, Pval], index = ['F-score', 'p-value'], columns = oligosList)
    #print(result)
    outputFile(result, file, oligosList)
    closeFunc()

if __name__ == "__main__":
    oligoslist = oligosList()
    file = input('Input data file path: ')
    main(file, oligoslist)  
