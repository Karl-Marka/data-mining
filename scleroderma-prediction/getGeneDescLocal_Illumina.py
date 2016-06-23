import pandas as pd

def closeFunc():
    print('''Type 'quit' and press enter to exit program''')
    answer = input(': ')
    if answer == 'quit':
        quit()
    else:
        closeFunc()

def oligosList():
    oligosPath = input('Path to the file containing the list of probes: ')
    oligos = open(oligosPath)
    oligos = oligos.readlines()
    oligosList = []
    for oligo in oligos:
        item = oligo.strip()
        oligosList.append(item)
    return oligosList



def main(oligosList, fullData = False):
    db = pd.read_csv('probes_illumina.txt', sep = '\t', header = 0, low_memory = False, index_col = 11)
    output = db.ix[oligosList]
    if fullData == False:
        output = output['Definition']
        print(output)
    else:
        output = output[['Accession', 'Symbol', 'Definition']]
    output.to_csv('getGeneDescLocal_results.txt', sep = '\t')
    closeFunc()
        

if __name__ == "__main__":
    oligosList = oligosList()
    answer = input('Do you want full data? (yes/no) ')
    if answer == 'no':
        main(oligosList)
    elif answer == 'yes':
        main(oligosList, True)
    else: 
        print('Wrong answer')
        closeFunc()