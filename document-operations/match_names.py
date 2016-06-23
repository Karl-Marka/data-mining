# This script matches the names from one file to the names and values in another file
import pandas as pd

def main(names, matches):
    names = pd.read_csv(names, sep = '\t', header = None)
    matches = pd.read_csv(matches, sep = '\t', header = None)
    nameslist = names[0].tolist()
    valueslist = names[1].tolist()
    dataJoined = pd.DataFrame(data = [])
    length = len(nameslist)
    for i,j in zip(nameslist, valueslist):
        dt = matches.loc[matches[0] == i]
        dt = dt[1].tolist()
        dt = str(dt[:1])        
        dt = dt.strip()
        dt = dt.replace('[', '')
        dt = dt.replace(']', '')
        dt = dt.replace("'", '')
        dt = pd.DataFrame([i, dt, j])
        dataJoined = pd.concat([dataJoined, dt.T])
        length -= 1
        if length % 30 == 0 :
            print(str(length) + ' items left to process')            
    dataJoined.to_csv("matched_result.txt", sep = '\t')    


if __name__ ==  "__main__" :
    names = input('Enter the path to the names file: ')
    matches = input('Enter the path to the file with the values to be matched: ')
    main(names, matches)