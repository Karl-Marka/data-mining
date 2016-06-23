from pandas import DataFrame, read_csv
from sklearn import linear_model
from math import exp

data = read_csv('Illumina_normalized_scaled.txt', header = 0, index_col = 0, sep = '\t')
data = data.T

oligos = ['ILMN_2154115', 'ILMN_1755115', 'ILMN_1661537', 'ILMN_1711516', 'ILMN_1767281', 'ILMN_1779813', 'ILMN_1699100', 'ILMN_1715393', 'ILMN_1789387', 'ILMN_1812877']
data = data[oligos]

model = read_csv('model_parameters_illumina.txt', header = 0, index_col = 0, sep = '\t')


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

f = open('predictions_list_illumina.txt', 'w')
f.write(predictions)
f.close()