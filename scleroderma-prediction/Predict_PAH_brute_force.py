from pandas import DataFrame, read_csv
from sklearn.cross_validation import train_test_split
import numpy as np
import random
from sklearn import linear_model


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


iters = 200
RSE = 10
turn = 1
combinations = []
RSSs = []
for i in range(0, 50000):
    for i in range(0,9):
        data = data.reindex(np.random.permutation(data.index))
    data2 = data.T    
    X_train, X_test, y_train, y_test = train_test_split(data2, labels, random_state=5)
    endindex =  random.randrange(10, 50, 1)
    X_train = X_train.iloc[:,0:endindex]
    X_test = X_test.iloc[:,0:endindex]
    clf.fit(X_train, y_train)
    train_predictions = clf.predict(X_train)
    test_predictions = clf.predict(X_test)
    in_sample_error = np.mean((train_predictions - y_train)**2)
    test_error = np.mean((test_predictions - y_test)**2)
    if test_error <= RSE:
        RSE = test_error
        best = X_train.columns.values
        best = best.tolist()
        combinations.append(best)
        RSSs.append(RSE)
        print('Turn:', turn, 'Current RSE:', test_error, 'Best RSE:', RSE)
    #print(train_predictions)
    #print(y_train)
    #print(in_sample_error)
    #print(test_error)    
    turn += 1

combinations_best = []
RSSs_best = []

for i in range(len(combinations)):
    if RSSs[i] <= RSE:
        combinations_best.append(combinations[i])
        RSSs_best.append(RSSs[i])

results = []
results_RSSs = []
lengths = []
combinations_best_sorted = sorted(combinations_best, key = len)
for j in combinations_best_sorted:
    if len(j) <= len(combinations_best_sorted[0]):
        results.append(j)
        results_RSSs.append(RSE)
        lengths.append(len(j))



shortest_combinations =  DataFrame(data = [results, lengths, results_RSSs], index = ['Combination', 'Length', 'RSS'], columns = None)
shortest_combinations = shortest_combinations.T
#print(shortest_combinations)

shortest_combinations.to_csv('shortest_combinations.txt', sep = '\t', index = False)
print(RSE)
closeFunc()
    
    

