from pandas import DataFrame, read_csv
from sklearn import linear_model
from math import exp

data = read_csv('x.txt', header = 0, index_col = 0, sep = '\t')
data = data.T

oligos = ['A_32_P30710', 'A_24_P148094', 'A_23_P77455', 'A_23_P148255', 'A_23_P141044', 'A_32_P103131', 'A_23_P121596', 'A_23_P24948', 'A_23_P68121', 'A_24_P396994']
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