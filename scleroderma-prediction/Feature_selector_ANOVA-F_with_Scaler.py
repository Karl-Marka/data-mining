#from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn.preprocessing import StandardScaler
import pandas as pd


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

def main(file):     
    data = pd.read_csv(file, sep='\t', header = 0, index_col = 0)
    #data = pd.DataFrame(data)
    #data = data.dropna(axis=1,how='all')
    classifier = data.tail(1)
    data = data.ix[:-1]
    classifier = classifier.unstack()
    header = data.columns
    oligosList = data.index
    stds = StandardScaler()
    data = stds.fit_transform(data)
    data = pd.DataFrame(data = data, columns = header, index = None)
    data = data.T
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
    file = input('Input data file path: ')
    main(file)  
