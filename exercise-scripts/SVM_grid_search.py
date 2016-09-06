from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np

def main():
    data = pd.read_csv('train.txt', header = 0, index_col = 0, sep = '\t')
    labels = pd.read_csv('labels_train.txt', header = None, sep = '\t')
    labels = labels.unstack().tolist()
    print(len(labels))
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size = 0.5, random_state=5)

    pipe_svc = Pipeline([('scl', StandardScaler()),
                ('clf', SVC(random_state=1))])

    param_range = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]
    gamma_range = [0.004, 0.04, 0.4]

    param_grid = [{'clf__C': param_range, 
                   'clf__kernel': ['linear']},
                  {'clf__C': param_range, 
                   'clf__gamma': gamma_range, 
                   'clf__kernel': ['rbf', 'poly', 'sigmoid']}]

    gs = GridSearchCV(estimator=pipe_svc, 
                    param_grid=param_grid, 
                    scoring='accuracy', 
                    cv=10,
                    n_jobs=-1,
                    verbose = 99)

    gs = gs.fit(X_train, y_train)
    predictions = gs.predict(X_test)
    MSE = np.mean((predictions - y_test)**2)
    #print(gs.best_score_)
    best_params = gs.best_params_
    print(best_params)
    print('Predicted labels:',predictions)
    print('True labels:',labels_test)
    print('MSE on the test set:',MSE)

    f = open('SVM.txt', 'w')
    for i in predictions:
        f.write("%s\n" % i)
    for j in labels_test:
        f.write("%s\n" % i)
    f.write("%s\n" % MSE)
    f.write("%s\n" % best_params)
    f.close()
    

if __name__ == "__main__":
    main()