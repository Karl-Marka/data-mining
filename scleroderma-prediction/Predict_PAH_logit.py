from pandas import DataFrame, read_csv
#from sklearn import linear_model
from math import exp

data = read_csv('./datasets/train_noduplicate.txt', header = 0, index_col = 0, sep = '\t')
data = data.T

oligos = ['ARL4C','AIF1','S100A11','MYOF','CYBB','LOC93622','LMO2','SLC31A2','FZD1','UPF3A','MS4A4A','SECTM1','C11orf75','DYSF','VRK2']
data = data[oligos]

model = read_csv('model_parameters.txt', header = 0, index_col = 0, sep = '\t')


patients = data.index.values
patients = patients.tolist()

predictions = []
coefs = []
intercept = model.ix['Intercept:']
for patient in patients:
    patientvalues = data.ix[patient]
    values = []        
    for i in oligos:
        value = patientvalues[i]
        coef = model.ix[i]
        values.append(value)
        coefs.append(coef)
    value = 0
    for x in range(len(values)):
        a = coefs[x] * values[x]
        value += a
    prediction = 1/(1 + exp(-(intercept + value)))
    print('Patient:', patient, 'Prediction:', prediction)
    predictions.append(str(prediction))        

predictions = ','.join(predictions)

f = open('predictions_list.txt', 'w')
f.write(predictions)
f.close()