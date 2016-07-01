print('Importing libraries')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import decomposition
from mpl_toolkits.mplot3d import Axes3D
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import f_classif
#from sklearn.externals import joblib

print('Reading data')
data = pd.read_csv('Illumina_normalized_symbols.txt', header = 0, index_col = 0, sep = '\t')
data = data.T
header = data.columns
index = data.index

stds = StandardScaler()
data = stds.fit_transform(data)
data = pd.DataFrame(data = data, columns = header, index = index)
data.T
le = LabelEncoder()


labels = pd.read_csv('labels.txt', header = None, index_col = None, sep = '\t')
labels = labels.unstack().tolist()

Sc_vs_all = ['Ssc' if i == 2 or i == 3 or i == 4 else 'All the rest' for i in labels]
PAH_vs_all = ['PAH' if i == 1 or i == 2 else 'All the rest' for i in labels]
ScPAH_vs_all = ['Ssc-PAH' if i == 2 else 'All the rest' for i in labels]
IPAH_vs_all = ['IPAH' if i == 1 else 'All the rest' for i in labels]
ScNoPAH_vs_all = ['Ssc_Non-PAH' if i == 3 or i == 3 else 'All the rest' for i in labels]
ILD_vs_all = ['ILD' if i == 4 else 'All the rest' for i in labels]
ScPAH_vs_IPAH_vs_all = ['Ssc-PAH' if i == 2 else 'IPAH' if i == 1 else 'All the rest' for i in labels]

conditions = [Sc_vs_all, PAH_vs_all, ScPAH_vs_all, IPAH_vs_all, ScNoPAH_vs_all, ILD_vs_all, ScPAH_vs_IPAH_vs_all]

for x in conditions:
    classes = set()
    for y in x:
        classes.add(y)
    classes = sorted(list(classes))    
    labels2 = le.fit_transform(x)
    labels2 = labels2.tolist()
    positive1 = labels2.count(1)
    positive2 = labels2.count(2)
    negative = labels2.count(0)
    all = len(labels2)
    data = stds.fit_transform(data)
    data = pd.DataFrame(data = data, columns = header, index = index)
    scores = f_classif(data, labels2)
    Fval = scores[0]
    Fval = Fval.tolist()
    Pval = scores[1]
    data_scores = data.copy()
    data_scores.ix['F'] = Fval 
    data_scores = data_scores.T   
    data_scores = data_scores.sort_values('F', axis = 0, ascending=False)
    #data_scores = data_scores.T
    del data_scores['F']
    l1 = 10
    l2 = 50
    l3 = 100
    l4 = 200
    l5 = 300
    data_top1 = data_scores.iloc[0:l1]
    data_top2 = data_scores.iloc[0:l2]
    data_top3 = data_scores.iloc[0:l3]
    data_top4 = data_scores.iloc[0:l4]
    data_top5 = data_scores.iloc[0:l5]
    datasets = [data_top1, data_top2, data_top3, data_top4, data_top5]
    for dataset in datasets:
        header2 = dataset.columns
        index2 = dataset.index
        dataset = stds.fit_transform(dataset)
        dataset = pd.DataFrame(data = dataset, columns = header2, index = index2)
        dataset.ix['L'] = labels2
        dataset = dataset.T
        dataset = dataset.sort_values('L', axis = 0)
        del dataset['L']
        #print(dataset)
        pca = decomposition.PCA()
        pca = pca.fit(dataset, labels2)
        #dataset.to_csv('dataset.txt', sep = '\t')
        #labels2 = pd.DataFrame(data = labels2)
        #labels2.to_csv('labels2.txt', sep = '\t')
        #joblib.dump(lda, './model/LDA_test.pkl') 
        X_pca = pca.transform(dataset)
        fig = plt.figure()
        fig = plt.figure(figsize=(10, 8), dpi=80)
        ax = fig.add_subplot(111, projection='3d')
        if len(classes) == 2:
            ax.scatter(X_pca[0:negative, 0], X_pca[0:negative, 1], X_pca[0:negative, 2], s=90, c = 'blue', depthshade=True, linewidths=0, label = classes[0])
            ax.scatter(X_pca[negative+1:all, 0], X_pca[negative+1:all, 1], X_pca[negative+1:all, 2], s=90, c = 'red', depthshade=True, linewidths=0, label = classes[1])
            plot_title = classes[1] + ' vs all the other classes with ' + str(len(dataset.columns)) + ' probes used'
            ax.set_title(plot_title) 
            filename = './plots/plot_' + classes[1] + '_vs_all' + str(len(dataset.columns)) + '_probes.png'                 
        elif len(classes) == 3:
            ax.scatter(X_pca[0:negative, 0], X_pca[0:negative, 1], X_pca[0:negative, 2], s=90, c = 'blue', depthshade=True, linewidths=0, label = classes[0])
            ax.scatter(X_pca[negative+1:positive2, 0], X_pca[negative+1:positive2, 1], X_pca[negative+1:positive2, 2], s=90, c = 'red', depthshade=True, linewidths=0, label = classes[1])
            ax.scatter(X_pca[positive2+1:all, 0], X_pca[positive2+1:all, 1], X_pca[positive2+1:all, 2], s=90, c = 'orange', depthshade=True, linewidths=0, label = classes[2])
            plot_title = classes[1] + ' vs ' + classes[2] + ' vs all the other classes with ' + str(len(dataset.columns)) + ' probes used'
            ax.set_title(plot_title) 
            filename = './plots/plot_' + classes[1] + '_vs_' + classes[2] + '_vs_all' + str(len(dataset.columns)) + '_probes.png' 
        ax.legend(loc = 'lower right')         
        fig.savefig(filename)   