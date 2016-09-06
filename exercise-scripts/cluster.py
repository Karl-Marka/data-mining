import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler

# 20 clusters

data = pd.read_csv("data.txt", header = 0, index_col = 0, sep = '\t')
data_numerical = data.iloc[:,0:16]
data_categorical = data.iloc[:,16:23]

header = data_numerical.columns
index = data_numerical.index

stds = StandardScaler()
stds = stds.fit(data_numerical)
data_numerical = stds.transform(data_numerical)

data_numerical = pd.DataFrame(data = data_numerical, columns = header, index = index)
data = pd.concat([data_numerical, data_categorical], axis = 1)

clusters = AgglomerativeClustering(n_clusters = 20).fit_predict(data)

f = open('clusters.txt', 'w')
for i in clusters:
  f.write("%s\n" % i)
f.close()

