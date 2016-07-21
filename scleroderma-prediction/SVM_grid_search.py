from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np

def main():
    data = pd.read_csv('./datasets/train_noduplicate_correl_60.txt', header = 0, index_col = 0, sep = '\t')
    if 'Rank' in data.columns:
        del data['Rank']
        print('Deleted Ranks')
    data = data.T
    probes = data.columns
    labels = pd.read_csv('./datasets/labels_train.txt', sep = '\t', header = None)
    labels = labels.unstack().tolist()
    test = pd.read_csv('./datasets/test_noduplicate.txt', header = 0, index_col = 0, sep = '\t')
    if 'Rank' in test.columns:
        del test['Rank']
        print('Deleted Ranks')
    test = test.T
    test = test[probes]
    labels_test = pd.read_csv('./datasets/labels_test.txt', header = None, sep = '\t')
    labels_test = labels_test.unstack().tolist()

    pipe_svc = Pipeline([('scl', StandardScaler()),
                ('clf', SVC(random_state=1))])

    param_range = [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]
    gamma_range = [0.00006, 0.0006, 0.006, 0.06, 0.6]

    param_grid = [{'clf__C': param_range, 
                   'clf__kernel': ['linear']},
                  {'clf__C': param_range, 
                   'clf__gamma': gamma_range, 
                   'clf__kernel': ['rbf', 'poly', 'sigmoid']}]

    gs = GridSearchCV(estimator=pipe_svc, 
                    param_grid=param_grid, 
                    scoring='accuracy', 
                    cv=10,
                    n_jobs=-1)

    gs = gs.fit(data, labels)
    predictions = gs.predict(test)
    MSE = np.mean((predictions - labels_test)**2)
    #print(gs.best_score_)
    print(gs.best_params_)
    print('Predicted labels:',predictions)
    print('True labels:',labels_test)
    print('MSE on the test set:',MSE)

    

if __name__ == "__main__":
    main()