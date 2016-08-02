import pandas as pd
import numpy as np

data = pd.read_csv('train.txt', header = 0, index_col = 0, sep = '\t')

parameters = list(data.columns)

correls = np.corrcoef(data, rowvar = 0)

result = pd.DataFrame(data=[], index = parameters, columns = parameters)

for parameter, correl in zip(parameters, correls):
    correl_values = list(correl)
    result[parameter] = correl_values

result.to_csv('correlations_matrix.txt', sep = '\t')

