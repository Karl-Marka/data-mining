import pandas as pd
from sklearn.feature_selection import RFECV
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler

data = pd.read_csv('./datasets/train_noduplicate.txt', header = 0, index_col = 0, sep = '\t')
data = data.T
header = data.columns
index = data.index
stds = StandardScaler()
data = stds.fit_transform(data)
data = pd.DataFrame(data = data, columns = header, index = index)
#data.T

labels = pd.read_csv('./datasets/labels_train.txt', sep = '\t', header = None)
labels = labels.unstack().tolist()

estimator = linear_model.LogisticRegression(random_state = 5, penalty = 'l2', C = 1.0)
selector = RFECV(estimator, step=1, cv=5, verbose = 1)
selector = selector.fit(data, labels)

ranking = selector.ranking_
ranking = list(ranking)
output = pd.DataFrame(data = ranking)

output.to_csv('./datasets/feature_ranking_logit_recursive.txt', sep = '\t', index = False)