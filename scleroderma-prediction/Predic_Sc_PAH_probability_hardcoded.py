print('Importing libraries')
from pandas import DataFrame, read_csv
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler
import numpy as np

oligos_sc = ['XIST','RPS4Y2','RPS4Y1','DDX3Y','MS4A4A','MYOF','ARL4C','VRK2','S100A11','FZD1','C11orf75','RAB15','LMO2','RCOR1','IGJ','DYSF','RAD51C','FCGR2A','ARHGEF10L','CYBB','KYNU','LOC93622','KIAA1522','42623','CTSB','DHRS7B','ACSL1','CSTB','PLA2G4A','UPF3A','SLC31A2','CAMKK2','CALML4','GNG5','C9orf167','CCR1','MZB1','C5orf32','CTNNA1','LOC100652840','GOLGA6L9','CHST15','TTTY14','CREB5','GLT1D1','WARS','ESRRA','SMPD4','ATP6V1B2','NAGK','TIMP2','VAMP5','TXNDC5','S100P','C2','PTX3','ANKS6','HMGB1','PDK4','CTSL1','RINT1','VPS37C','GRN','GLCCI1','STRBP']
oligos_PAH = ['ZBTB40','RBM17','TIMP1','FBRSL1','HSF2','GLOD4','ABLIM1','LOC390705','CEP72','ADM','ALAS2','BCAT1','TMEM158','ALKBH2','RASGRP1','MCM3','GSTO1','S100A10','ATP6V0A1','TMEM164','C12orf23','NSMCE4A','C5orf39','TRIB2','CORO1C','SELENBP1','LOC93622','SH3GLB1','MKL2','GEMIN4','EVL','GLUL','FBXO21','MRPL48','ZCWPW1','LGALS3','MSH2','LCK','CTNNA1','OCIAD2','PPP2R3B','SPEG','LBH','ANKS6','HAUS8','ZNF22','TYW1','CLEC2D','SEL1L3','ARHGEF4','NOSIP','SNCA','PUS1','PUM2','HADHB','SLC27A5','HIP1R','TNFAIP8','SFI1','IMPA2','DNMT1','MAGEH1','LEF1','SRGAP2','CTSB']
means = np.array([-7.2508,-2.67407778,-5.62846667,-2.86860556,-1.36541111,-2.36407778,-2.27974444,-5.01005,-5.50435556,-3.12296667,-3.05374444,-2.93088333,-1.52182778,-2.40443889,-3.25210556,-4.92518889,-5.2333,-3.55938333,-6.48432778,0.85436667,-6.50599444,-4.09310556,-1.67813333,-4.22541111,-1.22743889,-4.09716111,-4.39443889,-1.2018,-4.53074444,-6.02960556,-2.18221667,-3.76107778,-4.96255,-7.19313333,-4.23368889,-1.22635556,-2.65982778,-4.17452222,-3.95421667,-4.9353,-6.14138333,-1.45252222,-4.25641111,-6.76024444,-7.15746667,-5.63343889,-6.0523,-4.04338333,-5.3433,-7.43291111,-7.48360556,-3.60727222,-6.74832778,-0.52532778,-4.87527222,-5.70468889,-3.56868889,-5.40032778,-5.92549444,-4.02732778,-2.09643889,-4.24977222,-3.73610556,-3.35071667,-3.52974444])
scales = np.array([0.64012431,0.48644003,0.38126755,0.38895023,0.53052328,0.48778576,0.49807297,0.5971372,0.58102997,0.35492456,0.42872699,0.3511465,0.60229235,0.47275821,0.46769339,0.3230946,0.37759403,0.4308013,0.68179109,0.32208992,2.49611833,0.33738646,0.46875436,0.33033987,0.60419482,0.47778749,0.41107253,0.31601268,0.35915973,0.42817738,0.4227548,0.19555594,0.91245211,0.58704444,0.40104286,0.41405216,0.30157285,0.2961911,0.68120062,0.55607422,0.58102261,0.40702269,0.84641725,0.59481162,0.51046074,0.60413407,0.2918044,0.30595161,0.29806585,2.99733465,3.06453882,0.45402224,0.7214568,0.59115988,0.21016818,0.31385124,0.36536889,0.42501994,0.40787234,0.27886479,0.47295374,0.47554771,0.33143456,0.4482326,3.63471967])

means_PAH = np.array([-3.12208333,-7.10347222,-4.56233333,-5.44347222,-5.73447222,-5.58894444,-4.11030556,-7.18466667,-5.63466667,-1.85297222,-5.68872222,-1.34144444,-4.00611111,-5.16125,-3.47361111,-4.33552778,-2.92763889,-2.812,-4.59813889,-5.02736111,-4.17630556,-4.38347222,-4.799,-4.19444444,-5.13583333,-4.03788889,-4.57963889,-4.03633333,-1.48638889,-1.79041667,-3.42233333,-4.98155556,-4.90247222,-4.21816667,-3.31636111,-6.16036111,-5.82405556,-4.91691667,-6.05708333,-2.33216667,-4.39994444,-3.94036111,-4.83877778,-3.06369444,-4.32119444,-1.24025,-3.68625,-3.7015,-3.03108333,-5.59352778,-2.74713889,-4.115,-5.73516667,-4.15736111,-5.51825,-4.76769444,-4.45747222,-7.89680556,-3.50227778,-1.57858333,-4.51075,-4.25294444,-3.32391667,-3.70422222,-4.47977778])
scales_PAH = np.array([0.45548222,0.80531853,2.17800769,0.3312269,0.5574636,0.60266161,0.42579448,0.62891094,0.43979169,0.44390793,0.48784922,0.50522849,0.4829818,0.45891681,0.4967105,0.29290801,0.43744214,0.29929587,0.29863102,0.2803095,0.30981128,0.62333251,0.42782953,0.2712991,0.28531397,0.55639679,0.41519319,0.53463343,0.39496016,0.55651379,0.67715503,0.61693834,0.40185575,0.36765366,0.39692754,0.33544954,0.3896228,0.25982953,0.35702993,0.43382046,0.2227585,0.55168622,0.4477026,0.25315803,0.29330632,0.51658375,0.25700168,0.43494464,0.38839504,2.05306783,0.49589193,0.34088007,0.41657098,1.77035289,0.78410655,0.50427511,0.50024233,1.15517392,0.31911043,0.30325876,0.45989289,0.32215513,0.30175457,0.26866934,0.27823404])

print('Reading and normalizing data')
data = read_csv('./datasets/all_noduplicate.txt', header = 0, index_col = 0, sep = '\t')
test = data.ix[oligos_sc]
test_PAH = data.ix[oligos_PAH]
test = test.sort_index(axis = 0)
test_PAH = test_PAH.sort_index(axis = 0)
gene_exp = test.copy()
gene_exp_PAH = test_PAH.copy()
test = test.T
test_PAH = test_PAH.T
PAH_header = test_PAH.columns
PAH_index = test_PAH.index
header_test = test.columns
index_test = test.index
test = test.as_matrix()
test = np.array(test)
test = (test - means)/scales
test = DataFrame(data = test, columns = header_test, index = index_test)
test_PAH = test_PAH.as_matrix()
test_PAH = np.array(test_PAH)
test_PAH = (test_PAH - means_PAH)/scales_PAH
test_PAH = DataFrame(data = test_PAH, columns = PAH_header, index = PAH_index)
labels = read_csv('./datasets/labels_train.txt', sep = '\t', header = None)
labels = labels.unstack().tolist()
labels_test = read_csv('./datasets/labels_test.txt', sep = '\t', header = None)
labels_test = labels_test.unstack().tolist()
gene_data = read_csv('./datasets/gene_data.txt', header = 0, index_col = 0, sep = '\t')

intercept = 0.77777777777777823
coefs = [0.00098243,-0.0047879,0.03617133,-0.02130785,-0.02896074,0.04615671,-0.03039921,0.04184694,0.0391919,0.07393678,-0.05860535,-0.03349191,-0.05559615,-0.06198412,-0.0031149,0.00410208,-0.05777838,0.02920087,-0.00509455,0.06931355,-0.02210376,-0.02595638,0.0555343,-0.03700598,-0.01215271,0.07227833,0.02423346,0.01654485,0.03780628,-0.00961191,0.01403966,-0.05467147,-0.03159076,0.07839167,0.00365092,0.02541324,-0.01783945,-0.0125312,0.03157752,-0.02567822,-0.02937399,-0.05961683,-0.02032554,-0.02578202,-0.01745548,-0.02262699,-0.0886352,0.0191839,-0.05568611,-0.00835254,-0.02070594,0.02658609,-0.00396051,0.00763121,-0.03916338,0.02739357,-0.03501477,-0.01223597,-0.02754169,0.01253852,0.03934351,-0.00386323,0.12492334,0.03539774,0.02246754]
predictions = []

intercept_PAH = 0.33333333333333476
coefs_PAH = [0.00241079,-0.04230075,0.00515046,0.09402087,-0.0136427,0.02391159,0.03906091,0.13015909,-0.02400155,-0.15671898,-0.04971214,-0.00087562,-0.23052752,0.0503485,0.05411411,-0.1688456,0.04719709,-0.05567729,0.00108363,0.04508738,-0.07245604,0.00434705,0.00958327,0.04460761,0.01081198,0.0176367,-0.00435113,-0.06923663,-0.00033952,0.05871552,0.08685009,-0.0592945,-0.15864829,0.07290631,-0.04356502,-0.02311336,-0.06134274,-0.11681974,-0.05852237,-0.02166232,-0.14428914,0.03089396,0.1065567,0.04188958,0.05318762,-0.0847391,0.03926316,0.06534825,-0.04783862,0.04632451,0.19659504,0.2245639,0.00442051,-0.13100712,0.02495979,-0.11869847,-0.01535175,0.19565282,0.08549097,0.04298571,-0.04405261,-0.04324238,0.04641843,-0.00584063,-0.0739041]
predictions_PAH = []

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

for patient_PAH in gene_exp_PAH.columns:
    values = test_PAH.ix[patient_PAH]
    values = values.tolist()
    print(values)
    value = 0    
    for y in range(len(values)):
        a = coefs_PAH[y] * values[y]
        value += a
    prediction = intercept_PAH + value
    if prediction <= 0.1:
        predictions_PAH.append('< 10%')
    elif prediction <= 0.3:
        predictions_PAH.append('< 30%')
    elif prediction <= 0.5:
        predictions_PAH.append('< 50%')
    elif prediction <= 0.75: 
        predictions_PAH.append('75%')
    elif prediction <= 0.9:
        predictions_PAH.append('90%')
    elif prediction > 0.9:
        predictions_PAH.append('> 90%')    

predictions = dict(zip(index_test, predictions))
predictions_PAH = dict(zip(PAH_index, predictions_PAH))
#print(predictions_PAH)

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
    PAH_probability = predictions_PAH.get(patient)
    if float(predictions.get(patient)) >= 0.5:
        if probability < 50:
           print('Patient',patient,'is Scleroderma negative') 
        if 70 > probability >= 50 :
            print('Patient',patient,'is borderline with a gene exp. similiarity of',probability,'% to a reference Scleroderma gene exp. pattern. The probability for PAH is:',PAH_probability)
        elif probability >= 70 :
            print('Patient',patient,'is Scleroderma positive with a gene exp. similiarity of',probability,'% to a reference Scleroderma gene exp. pattern. The probability for PAH is:',PAH_probability)              
    elif float(predictions.get(patient)) < 0.5 :
        print('Patient',patient,'is Scleroderma negative')
        



