import pandas as pd

print('Removes rows that contain NaN-s from a tab-separated file')
print('Assumes the first row is header')
print(' ')
file = input('Path to input data file: ')
data = pd.read_csv(file, sep='\t', header = None, index_col = 0, low_memory = False)
data = pd.DataFrame(data)
data = data.dropna()
data.columns = [data.ix[0]]
data = data.drop(data.index[0])

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