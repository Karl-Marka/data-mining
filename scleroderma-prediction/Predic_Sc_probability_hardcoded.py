print('Importing libraries')
from pandas import DataFrame, read_csv
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler
import numpy as np

means = np.array([-7.2508,-2.67407778,-5.62846667,-2.86860556,-1.36541111,-2.36407778,-2.27974444,-5.01005,-5.50435556,-3.12296667,-3.05374444,-2.93088333,-1.52182778,-2.40443889,-3.25210556,-4.92518889,-5.2333,-3.55938333,-6.48432778,0.85436667,-6.50599444,-4.09310556,-1.67813333,-4.22541111,-1.22743889,-4.09716111,-4.39443889,-1.2018,-4.53074444,-6.02960556,-2.18221667,-3.76107778,-4.96255,-7.19313333,-4.23368889,-1.22635556,-2.65982778,-4.17452222,-3.95421667,-4.9353,-6.14138333,-1.45252222,-4.25641111,-6.76024444,-7.15746667,-5.63343889,-6.0523,-4.04338333,-5.3433,-7.43291111,-7.48360556,-3.60727222,-6.74832778,-0.52532778,-4.87527222,-5.70468889,-3.56868889,-5.40032778,-5.92549444,-4.02732778,-2.09643889,-4.24977222,-3.73610556,-3.35071667,-3.52974444])
scales = np.array([0.64012431,0.48644003,0.38126755,0.38895023,0.53052328,0.48778576,0.49807297,0.5971372,0.58102997,0.35492456,0.42872699,0.3511465,0.60229235,0.47275821,0.46769339,0.3230946,0.37759403,0.4308013,0.68179109,0.32208992,2.49611833,0.33738646,0.46875436,0.33033987,0.60419482,0.47778749,0.41107253,0.31601268,0.35915973,0.42817738,0.4227548,0.19555594,0.91245211,0.58704444,0.40104286,0.41405216,0.30157285,0.2961911,0.68120062,0.55607422,0.58102261,0.40702269,0.84641725,0.59481162,0.51046074,0.60413407,0.2918044,0.30595161,0.29806585,2.99733465,3.06453882,0.45402224,0.7214568,0.59115988,0.21016818,0.31385124,0.36536889,0.42501994,0.40787234,0.27886479,0.47295374,0.47554771,0.33143456,0.4482326,3.63471967])

print('Reading and normalizing data')
train = read_csv('./datasets/train_noduplicate_scores_top10pc.txt', header = 0, index_col = 0, sep = '\t')
train = train.sort_index(axis = 0)
train = train.T
header = train.columns
index = train.index
train = train.as_matrix()
train = np.array(train)
train = (train - means)/scales
train = DataFrame(data = train, columns = header, index = index)
test = read_csv('./datasets/test_noduplicate_scores_top10pc.txt', header = 0, index_col = 0, sep = '\t')
test = test.sort_index(axis = 0)
gene_exp = test.copy()
test = test.T
header_test = test.columns
index_test = test.index
test = test.as_matrix()
test = np.array(test)
test = (test - means)/scales
test = DataFrame(data = test, columns = header_test, index = index_test)
labels = read_csv('./datasets/labels_train.txt', sep = '\t', header = None)
labels = labels.unstack().tolist()
labels_test = read_csv('./datasets/labels_test.txt', sep = '\t', header = None)
labels_test = labels_test.unstack().tolist()
gene_data = read_csv('./datasets/gene_data.txt', header = 0, index_col = 0, sep = '\t')

intercept = 0.77777777777777823
coefs = [0.00098243,-0.0047879,0.03617133,-0.02130785,-0.02896074,0.04615671,-0.03039921,0.04184694,0.0391919,0.07393678,-0.05860535,-0.03349191,-0.05559615,-0.06198412,-0.0031149,0.00410208,-0.05777838,0.02920087,-0.00509455,0.06931355,-0.02210376,-0.02595638,0.0555343,-0.03700598,-0.01215271,0.07227833,0.02423346,0.01654485,0.03780628,-0.00961191,0.01403966,-0.05467147,-0.03159076,0.07839167,0.00365092,0.02541324,-0.01783945,-0.0125312,0.03157752,-0.02567822,-0.02937399,-0.05961683,-0.02032554,-0.02578202,-0.01745548,-0.02262699,-0.0886352,0.0191839,-0.05568611,-0.00835254,-0.02070594,0.02658609,-0.00396051,0.00763121,-0.03916338,0.02739357,-0.03501477,-0.01223597,-0.02754169,0.01253852,0.03934351,-0.00386323,0.12492334,0.03539774,0.02246754]
predictions = []


for patient in gene_exp.columns:
    values = test.ix[patient]
    values = values.tolist()
    value = 0    
    for x in range(len(values)):
        a = coefs[x] * values[x]
        value += a
    prediction = intercept + value
    #print('Patient:', patient, 'Prediction:', prediction)
    predictions.append(str(prediction)) 


predictions = dict(zip(index_test, predictions))

up = dict()
down = dict()

for i in gene_data.index:
    condition = gene_data.loc[i,'condition']
    value = gene_data.loc[i,'value']
    if condition == 'UP':
        up.update({i : value})
    elif condition == 'DOWN':
        down.update({i : value})

for patient in gene_exp.columns:
    score = 0
    data = gene_exp[patient]
    for gene in data.index:
        if gene in up.keys():
            if data.ix[gene] > up.get(gene):
                score += 1
        elif gene in down.keys():
            if data.ix[gene] < down.get(gene):
                    score += 1
    probability = int(round((score/65)*100,0))
    if float(predictions.get(patient)) >= 0.5:
        if probability < 50:
           print('Patient',patient,'is Scleroderma negative') 
        if 70 > probability >= 50 :
            print('Patient',patient,'is borderline with a gene exp. similiarity of',probability,'% to a reference Scleroderma gene exp. pattern')
        elif probability >= 70 :
            print('Patient',patient,'is Scleroderma positive with a gene exp. similiarity of',probability,'% to a reference Scleroderma gene exp. pattern')              
    elif float(predictions.get(patient)) < 0.5 :
        print('Patient',patient,'is Scleroderma negative')
        



