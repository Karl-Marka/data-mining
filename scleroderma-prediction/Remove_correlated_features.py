import pandas as pd
import numpy as np

print('Reading data')
data = pd.read_csv('./datasets_large/train.txt', header = 0, index_col = 0, sep = '\t')
matrix = pd.read_csv('correlations_matrix.txt', header = 0, index_col = 0, sep = '\t')

threshold_pos = 0.5
threshold_neg = -0.5

probes = data.index.tolist()

print('Iterating through values')

counter = len(data.index)
for probe in data.index:
    if probe in probes:
        row = matrix.ix[probe]
        for probe2 in row.index:
            if probe2 != probe and probe2 in probes:
                value = row[probe2]
                if value > threshold_pos or value < threshold_neg:
                    probes.remove(probe2)
    counter -= 1
    print(counter, 'Probes left')


#probes_ok = list(probes)
result = data.ix[probes]

result.to_csv('result_remove_correlated_features.txt', sep = '\t')
    