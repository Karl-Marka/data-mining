from pandas import DataFrame, read_csv
from sklearn.cross_validation import train_test_split
from sklearn.feature_selection import f_classif
import matplotlib.pyplot as plt
from numpy import mean, array
from sklearn import linear_model
from pylab import figure, xlim, ylim, ylabel, xlabel, title, tick_params, axvspan, gca, plot, figtext, subplot, legend
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

data = read_csv('x.txt', header = 0, index_col = 0, sep = '\t')
data = data.T
#print(X.head(2))
labels = read_csv('y.txt', header = None, sep = '\t')
labels = labels.unstack().tolist()
#print(Y)

result = f_classif(data, labels)
Fval = result[0]
Fval = list(Fval)
data.ix['F'] = Fval
data = data.T
data = data.sort_values('F', axis = 0, ascending=False)
data = data.T
data = data.drop(['F'])

def closeFunc():
    print('''Type 'quit' and press enter to exit program''')
    answer = input(': ')
    if answer == 'quit':
        quit()
    else:
        closeFunc()

noOfOligos = len(data.columns)
#noOfOligos = 100
clf = linear_model.LogisticRegression(random_state = 5)

in_sample_errors = []
test_errors = []

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

RSE = 1
turn = 1
while turn < (noOfOligos - 1):    
    X_train, X_test, y_train, y_test = train_test_split(data, labels, random_state=5)
    result = f_classif(X_train, y_train)
    Fval = result[0]
    Fval = list(Fval)
    X_train.ix['F'] = Fval
    X_test.ix['F'] = Fval
    X_train = X_train.T
    X_test = X_test.T
    X_train = X_train.sort_values('F', axis = 0, ascending=False)
    X_test = X_test.sort_values('F', axis = 0, ascending=False)
    X_train = X_train.T
    X_test = X_test.T
    X_train = X_train.drop(['F'])
    X_test = X_test.drop(['F'])
    X_train = X_train.iloc[:,0:turn]
    X_test = X_test.iloc[:,0:turn]
    clf.fit(X_train, y_train)
    train_predictions = clf.predict(X_train)
    test_predictions = clf.predict(X_test)
    in_sample_error = mean((train_predictions - y_train)**2)
    test_error = mean((test_predictions - y_test)**2)
    if test_error < RSE:
        RSE = test_error
    in_sample_errors.append(in_sample_error)
    test_errors.append(test_error)
    #print(train_predictions)
    #print(y_train)
    #print(in_sample_error)
    #print(test_error)
    print((noOfOligos-turn), 'Parameters left.', 'Current RSE:', RSE)
    turn += 1

#in_sample_errors = array(in_sample_errors)
#test_errors = array(test_errors)
#print(in_sample_errors)
#print(test_errors)
createPlot(in_sample_errors, test_errors, noOfOligos-1)
print(RSE)
closeFunc()
    
    

