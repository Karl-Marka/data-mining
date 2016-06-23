from pandas import read_csv, concat, DataFrame, Series
from math import exp
from sklearn.externals import joblib
from sklearn import svm

probeList = ['A_23_P214627','A_23_P145863','A_23_P86682','A_23_P126593','A_23_P354387','A_23_P53126','A_23_P50498','A_23_P75430','A_23_P204847','A_23_P202672','A_24_P38276','A_32_P43664','A_23_P358957','A_23_P154894','A_23_P317620','A_23_P56898','A_23_P215944','A_23_P65651','A_23_P217109','A_23_P75769','A_23_P167168','A_23_P69491']

def readFile(filename, dropLast = True):
    geneExp = read_csv(filename, sep="\t", header = 0, index_col = '0')   
    #print(geneExp.head(10))
    dataCropped = DataFrame(data=[])
    for probe in probeList:
        dt = geneExp.ix[probe]
        dataCropped = concat([dataCropped, dt], axis = 1)
    # dropping last two columns
    if dropLast == True :
        dataCropped = dataCropped.drop(labels=['F-score', 'p-value'], axis=0)
        return dataCropped
    else:
        return dataCropped 

def decisionTree(data):
    results = dict()
    for row in data.itertuples():
        index = row[0]
        first = row[1]
        second = row[2]
        third = row[3]
        fourth = row[4]
        fifth = row[5]
        if first > 1.4 :
            if second > 3.8:
                results.update({index: "positive"})
            else:
                if third > 1.6:
                    results.update({index: "positive"})
                else:
                    if fourth > 4.7 :
                        results.update({index: "positive"})
                    else:
                        if fifth > 1.5 :
                            results.update({index: "positive"})
                        else:
                            results.update({index: "negative"})
        else:
            if second > 4:
                results.update({index: "positive"})
            else:
                if third > 1.9:
                    results.update({index: "positive"})
                else:
                    if fourth > 5 :
                        results.update({index: "positive"})
                    else:
                        if fifth > 1.5 :
                            results.update({index: "positive"})
                        else:
                            results.update({index: "negative"})            
    return results
  
def consensualScore(data):
    upReg = {'A_23_P214627': 4.453337186, 'A_23_P145863': 3.711519199, 'A_23_P86682': 2.644986161, 'A_23_P126593': 3.125354821, 'A_23_P354387': 3.365771812, 'A_23_P53126': 3.757735849}
    downReg = {'A_32_P43664': 3.051606459, 'A_23_P317620': 7.226355612, 'A_23_P167168': 4.511587486}
    result = dict()      
    for row in data.itertuples():
        score = 0
        id = row[0]
        row = row._asdict()      
        for key in row:
            value = row.get(key)
            if key in upReg.keys():
                refValue = upReg.get(key)
                if value >= refValue:
                    score += 1
                else: 
                    score -= 1
            elif key in downReg.keys():
                refValue = downReg.get(key)
                if value >= refValue:
                    score -= 1
                else:
                    score += 1
            else:
                refValue = 0
        result.update({id: score})
    return result                 

def logit(patientID, data, threshold):
    data = data.ix[patientID]
    #print(data)
    coefs = {'A_23_P214627': -0.22058043,'A_23_P145863': 0.06020512,'A_23_P86682': 0.32085253,'A_23_P126593': 0.01974147,'A_23_P354387': 0.13316079,'A_23_P53126': -0.02548267,'A_23_P50498': -0.00639148,'A_23_P75430': -0.37544548,'A_23_P204847': 0.29141421,'A_23_P202672': 0.32923712,'A_24_P38276': 0.07158979,'A_32_P43664': -0.33490231,'A_23_P358957': 0.14300184,'A_23_P154894': 0.27095627,'A_23_P317620': -0.25548039,'A_23_P56898': -0.30362185,'A_23_P215944': 0.14448303,'A_23_P65651': 0.45106354,'A_23_P217109': -0.23809546,'A_23_P75769': -0.24049614, 'A_23_P167168': 0, 'A_23_P69491': 0}
    intercept = -0.05444707
    sum = 0
    for probe in probeList:
        value = data.ix[probe]
        coef = coefs.get(probe)
        sum += value * coef
    score = 1/(1 + exp(-(intercept + sum)))
    if score >= threshold :
        return "Borderline - positive"
    else:
        return "Borderline - negative" 

def svm(patientID, data):
    data = data.ix[patientID]
    oligos = ['A_23_P214627','A_23_P145863','A_23_P86682','A_23_P126593','A_23_P354387','A_23_P53126','A_23_P50498','A_23_P75430','A_23_P204847','A_23_P202672','A_24_P38276','A_32_P43664','A_23_P358957','A_23_P154894','A_23_P56898','A_23_P215944','A_23_P65651','A_23_P217109','A_23_P75769','A_23_P69491']       
    data = data[oligos]
    data = data.reshape(1, -1)
    #print(data)
    clf = joblib.load('./model/svm_rbf.pkl')
    prediction = clf.predict(data)
    if prediction == 1:
        return "Borderline - positive"
    else:
        return "Borderline - negative"

def main(scores):
    output = DataFrame(data = [])
    for i in scores.keys():
        #print(i)
        #print(scores.get(i))
        value = scores.get(i)
        if value >= 4 :
            prediction = "Positive"
        elif 2 < value < 4 :
            prediction = str(svm(i, data))
            #print(logit(i, data))
        elif 0 < value <= 2 :
            prediction = str(logit(i, data, 0.8))
        elif value <= 0 :
            prediction = "Negative"
        else:
            prediction = "Not calculated"
        print(str(i) + ' ' + prediction)
        row = Series(data = [i, value, prediction])
        output = concat([output, row], axis = 1)
    output = output.T
    output.to_csv("consensus_predictions.txt", sep = '\t')

def closeFunc():
    print('''Type 'quit' and press enter to exit program''')
    answer = input(': ')
    if answer == 'quit':
        quit()
    else:
        closeFunc()        

if __name__ == "__main__":
    file = input("Input gene expression values file: ") 
    data = readFile(file, False)
    scores = consensualScore(data)
    main(scores)
    closeFunc()     