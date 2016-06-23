from pandas import DataFrame, read_csv
from sklearn.cross_validation import train_test_split
from sklearn.feature_selection import f_classif
import matplotlib.pyplot as plt
import numpy as np
import random
from sklearn import linear_model
from pylab import figure, xlim, ylim, ylabel, xlabel, title, tick_params, axvspan, gca, plot, figtext, subplot, legend
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

data = read_csv('x.txt', header = 0, index_col = 0, sep = '\t')
#data = data.T
#print(X.head(2))
labels = read_csv('y.txt', header = None, sep = '\t')
labels = labels.unstack().tolist()
#print(Y)

noOfOligos = len(data.columns)
#noOfOligos = 100
clf = linear_model.LogisticRegression(random_state = 5)


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
    print(x)
    xlabel("No. of parameters")
    ylabel("R-squared error")
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
    fig.savefig('PAH_errorgraph.png')

iters = 200
RSE = 10
turn = 1
best = list(range(0,100))
while RSE > 0.07:
    data2 = data.reindex(np.random.permutation(data.index))
    data2 = data2.T    
    X_train, X_test, y_train, y_test = train_test_split(data2, labels, random_state=5)
    endindex =  random.randrange(30, 55, 1)
    X_train = X_train.iloc[:,0:endindex]
    X_test = X_test.iloc[:,0:endindex]
    clf.fit(X_train, y_train)
    train_predictions = clf.predict(X_train)
    test_predictions = clf.predict(X_test)
    in_sample_error = np.mean((train_predictions - y_train)**2)
    test_error = np.mean((test_predictions - y_test)**2)
    if test_error < RSE and len(X_train.columns.values) < len(best):
        RSE = test_error
        best = X_train.columns.values
    #print(train_predictions)
    #print(y_train)
    #print(in_sample_error)
    #print(test_error)
    print('Turn:', turn, 'Current RSE:', RSE)
    turn += 1


print(RSE)
best = best.tolist()
best.append(str(RSE))
best = ','.join(best)
f = open('best_predictors_RSE.txt', 'w')
f.write(best)
f.close()
closeFunc()
    
    

