from pandas import DataFrame, read_csv
from scipy.spatial.distance import pdist, squareform
from sklearn.preprocessing import StandardScaler

data = read_csv('./datasets/all.txt', header = 0, index_col = 0, sep = '\t')
data = data.T
header = data.columns
index = data.index
stds = StandardScaler()
data = stds.fit_transform(data)
data_transposed = DataFrame(data = data, columns = header, index = index)
data = data.T
labels = data_transposed.index
labels_probes = data_transposed.columns

row_dist_samples = DataFrame(squareform(pdist(data_transposed, metric = 'euclidean')), columns = labels, index = labels)
row_dist_probes = DataFrame(squareform(pdist(data, metric = 'euclidean')), columns = labels_probes, index = labels_probes)

row_dist_samples.to_csv('Distances_samples.txt', sep = '\t')
row_dist_probes.to_csv('Distances_probes.txt', sep = '\t')