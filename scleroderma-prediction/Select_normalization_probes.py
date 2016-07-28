import pandas as pd
import numpy as np
import scipy.stats as sp

data = pd.read_csv('./datasets_PAH/all_noduplicate.txt', header = 0, index_col = 0, sep = '\t')
data = data.T

CV = np.absolute(sp.variation(data, axis=0))

data.ix['CV'] = CV

data = data.T
data_sorted = data.sort_values('CV', axis = 0, ascending = True)
data = data.T
data_sorted = data_sorted.T

best = data_sorted.iloc[:,0]
del best['CV']
best_name = data_sorted.columns[0] 

best = np.mean(list(best))

data_means = np.mean(data, axis = 0)

data.ix['mean'] = data_means

data = data.T
data = data.sort_values('CV', axis = 0, ascending = True)
data = data.T

del data[best_name]

best_probes = []

for i in range(5):
    st_dev = 10
    probe_select = ''
    for probe in data:
        mean = data.loc['mean',probe]
        st_dev_current = float(np.std([best, mean]))
        if st_dev_current < st_dev:
            st_dev = st_dev_current
            probe_select = probe
    print('Probe:',probe_select,'St.Dev:',st_dev)
    del data[probe_select]
    



'''
data_means = pd.DataFrame(data_means, columns = ['mean'])
data_means = data_means.sort_values('mean', axis = 0, ascending = True)

best_loc = data_means.index.get_loc(best_name)
'''
