import numpy as np
import pandas as pd
from sklearn import decomposition
from sklearn.externals import joblib

train = pd.read_csv('Illumina_normalized_scaled.txt', sep = '\t', header = 0, index_col = 0)
train = train.T

pca = decomposition.PCA()
pca.fit(train)

joblib.dump(pca, './model/PCA.pkl') 