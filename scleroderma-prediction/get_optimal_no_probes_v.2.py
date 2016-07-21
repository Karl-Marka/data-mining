from pandas import DataFrame, read_csv
from sklearn.cross_validation import train_test_split
from sklearn.feature_selection import f_classif
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from pylab import figure, xlim, ylim, ylabel, xlabel, title, tick_params, axvspan, gca, plot, figtext, subplot, legend
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from sklearn.preprocessing import StandardScaler

def readfiles():
    dataset = input("Input the data file location: ")
    labelsfile = input("Input the labels file location: ")
    data = read_csv(dataset, header = 0, index_col = 0, sep = '\t')
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
    labels = read_csv(labelsfile, header = None, sep = '\t')
    labels = labels.unstack().tolist()
    return data, labels


def closeFunc():
    print('''Type 'quit' and press enter to exit program''')
    answer = input(': ')
    if answer == 'quit':
        quit()
    else:
        closeFunc()

def movingaverage(interval, window_size):
    # Calculates the moving average of window_size points for a list or array
    window = np.ones(int(window_size))/float(window_size)
    result = np.convolve(interval, window, 'same')
    return result

def createPlot(y1, y2, limit, filename, highestMSE_probes, lowestMSE_probes, highestMSE, lowestMSE):
    xFormatter = FormatStrFormatter('%d')
    fig = figure()     
    xlim(1, limit-10)
    x = list(range(1,limit))
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
    content = "Highest MSE (" + str(highestMSE) + ") at: " + str(highestMSE_probes) + " parameters. Lowest MSE (" + str(lowestMSE) + ") at: " + str(lowestMSE_probes) + " parameters"
    figtext(.05, .05, content)
    ax = subplot(111)
    plot(x, y1, 'orange', label = 'In-sample error')
    plot( x, y2, 'red', label = 'Testing error')
    ax.xaxis.set_major_formatter(xFormatter)
    legend(bbox_to_anchor=(0.85, 0.75), loc=4, borderaxespad=0.1)
    fig.savefig(filename)


def main(data, labels, noOfOligos = 0, positive_threshold = 0.5):
    if noOfOligos == 0:
        noOfOligos = len(data.columns)
    noOfOligos = int(noOfOligos)
    positive_threshold = float(positive_threshold)
    print('Number of probes to plot:',noOfOligos)
    print('Positive threshold:', positive_threshold)
    #clf = linear_model.LogisticRegression(random_state = 5, penalty = 'l1', C = 1000.0)
    clf = linear_model.LinearRegression()
    y1 = []
    y2 = []
    lowestMSE = 1000
    lowestMSE_probes = 0
    highestMSE = 0
    highestMSE_probes = 0
    worstPredictions = []
    for i in range(1,noOfOligos+1):    
        data_current = data.iloc[:,0:i] 
        sum_sample_errors = 0
        sum_test_errors = 0
        for j in range(10):
            seed = np.random.randint(0,10) 
            X_train, X_test, y_train, y_test = train_test_split(data_current, labels, test_size = 0.5, random_state=seed)
            clf.fit(X_train, y_train)
            train_predictions = clf.predict(X_train)
            train_predictions = [1 if i > positive_threshold else 0 for i in train_predictions]
            test_predictions = clf.predict(X_test)
            test_predictions = [1 if i > positive_threshold else 0 for i in test_predictions]
            sum_sample_errors += np.mean([(a - b)**2 for a, b in zip(train_predictions,y_train)])
            sum_test_errors += np.mean([(a - b)**2 for a, b in zip(test_predictions,y_test)])
        in_sample_error = sum_sample_errors/10
        test_error = sum_test_errors/10
        if test_error < lowestMSE:
            lowestMSE = test_error
            lowestMSE_probes = i
        elif test_error > highestMSE:
            highestMSE = test_error
            highestMSE_probes = i      
        y1.append(in_sample_error)
        y2.append(test_error)
        #print(in_sample_error)
        #print(test_error)
        print('Currently at turn:',i)
        #print('Length test labels:',len(y_test))
        #print('Length predictions:',len(test_predictions))
    print("Highest MSE:",highestMSE,"at:",highestMSE_probes,"probes")
    print("Lowest MSE:",lowestMSE,"at:",lowestMSE_probes,"probes")
    if noOfOligos <= 100:
        y2 = movingaverage(y2, 5)
    elif noOfOligos <= 300:
        y2 = movingaverage(y2, 10)
    elif noOfOligos <= 500:
        y2 = movingaverage(y2, 20)
    elif noOfOligos <= 1000:
        y2 = movingaverage(y2, 40)
    else:
        y2 = movingaverage(y2, 100)
    lowestMSE = round(lowestMSE, 4)
    highestMSE = round(highestMSE, 4)        
    #y2 = movingaverage(y2, 10)
    filename = "plot_MSE_" + str(noOfOligos) + "_probes.png"
    createPlot(y1, y2, noOfOligos+1, filename, highestMSE_probes, lowestMSE_probes, highestMSE, lowestMSE)
    closeFunc()


if __name__ == "__main__":
    data, labels = readfiles()
    no_oligos = input('Specify the number of probes to plot (0 for all) ')
    threshold = input('Specify the threshold for positive predictions in the model (0 = default) ')
    if no_oligos == '0'  and threshold == '0':
        main(data, labels)
    elif no_oligos != '0'  and threshold == '0':
        main(data, labels, no_oligos)
    else:
        main(data, labels, no_oligos, threshold)
        