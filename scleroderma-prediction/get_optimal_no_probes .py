from pandas import DataFrame, read_csv
from sklearn.cross_validation import train_test_split
from sklearn.feature_selection import f_classif
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from pylab import figure, xlim, ylim, ylabel, xlabel, title, tick_params, axvspan, gca, plot, figtext, subplot, legend
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from sklearn.preprocessing import StandardScaler

data = read_csv('./datasets/train_noduplicate_ranked.txt', header = 0, index_col = 0, sep = '\t')
if 'Rank' in data.columns:
    data = data.sort_values('Rank', axis = 0, ascending=True)
    del data['Rank']
    print('Deleted the Rank columns')
data = data.T
header = data.columns
index = data.index
stds = StandardScaler()
data = stds.fit_transform(data)
data = DataFrame(data = data, columns = header, index = index)


labels = read_csv('./datasets/labels_train.txt', header = None, sep = '\t')
labels = labels.unstack().tolist()


#noOfOligos = len(data.columns)
noOfOligos = 100
#clf = linear_model.LogisticRegression(random_state = 5, penalty = 'l1', C = 1000.0)
clf = linear_model.LinearRegression()


def closeFunc():
    print('''Type 'quit' and press enter to exit program''')
    answer = input(': ')
    if answer == 'quit':
        quit()
    else:
        closeFunc()

def createPlot(y1, y2, limit):
    xFormatter = FormatStrFormatter('%d')
    fig = figure()     
    xlim(1, limit)
    x = list(range(1,limit))
    #print(x)
    xlabel("No. of parameters")
    ylabel("Mean squared error")
    title("In-sample error and testing error")
    tick_params(
        axis='x',          
        which='both',     
        bottom='off',      
        top='off',        
        labelbottom='on') 
    gca().set_position((.1, .3, .8, .6)) 
    #figtext(.04, .05, content)
    ax = subplot(111)
    plot(x, y1, 'orange', label = 'In-sample error')
    plot( x, y2, 'red', label = 'Testing error')
    ax.xaxis.set_major_formatter(xFormatter)
    legend(bbox_to_anchor=(0.85, 0.75), loc=4, borderaxespad=0.1)
    fig.savefig('training_testing_errors.png')

y1 = []
y2 = []

for i in range(1,noOfOligos):    
    data_current = data.iloc[:,0:i] 
    sum_sample_errors = 0
    sum_test_errors = 0
    for j in range(0,100):
        seed = np.random.randint(0,10) 
        X_train, X_test, y_train, y_test = train_test_split(data_current, labels, test_size = 0.5, random_state=seed)
        clf.fit(X_train, y_train)
        train_predictions = clf.predict(X_train)
        test_predictions = clf.predict(X_test)
        sum_sample_errors += np.mean((train_predictions - y_train)**2)
        sum_test_errors += np.mean((test_predictions - y_test)**2)
    in_sample_error = sum_sample_errors/10
    test_error = sum_test_errors/10
    y1.append(in_sample_error)
    y2.append(test_error)
    #print(in_sample_error)
    #print(test_error)
    print('Currently at turn:',i)

createPlot(y1, y2, noOfOligos)
closeFunc()