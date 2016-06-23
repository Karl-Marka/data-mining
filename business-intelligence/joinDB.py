# Concatenates .csv files together based on a common header
from pandas import DataFrame, concat, read_csv
import os

def noOfFiles():
    count = 0
    for file in os.listdir("./join"):
        if file.endswith(".csv"):
            count += 1
    return count

def fileNames():
    files = []
    for file in os.listdir("./join"):
        if file.endswith(".csv"):
            files.append(file)
    for i in files:
        yield i

def closeFunc():
    print('''Type 'quit' and press enter to exit program''')
    answer = input(': ')
    if answer == 'quit':
        quit()
    else:
        closeFunc()

def main(filenames, count, header):
    output = DataFrame(data = [], columns = header)
    for x in range(0, count):        
        filename = './join/' + next(filenames)
        print('Adding',filename)
        file = read_csv(filename, header = 0, sep = ',', low_memory = False)
        oldindex = file.columns
        oldindex = oldindex.tolist()
        print('Length:',str(len(file.index)),'rows')
        newfile = DataFrame(data = [])
        for title in header:
            if title in oldindex:
                newfile[title] = file[title]
            else:
                newfile[title] = ""
        file = None
        output = concat([output,newfile])
    print(str(len(output.index)),'total rows added')    
    output.to_csv("./join/joined_result.txt", sep = '\t', index = False)
    output = None
    print('Output written to: /join/joined_result.txt')
    closeFunc()               
        
if __name__ == "__main__":
    print('This script concatenates several .csv files together based on a common header.')
    print('The header file must also be in .csv format.')
    headerfile = input('Specify the common header file to use: ')    
    header = read_csv(headerfile, header = None, sep = ',')
    header = header.unstack().tolist()
    filenames = fileNames()
    count = noOfFiles()
    main(filenames, count, header)
   
