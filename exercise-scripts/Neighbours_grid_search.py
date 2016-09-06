from sklearn.grid_search import GridSearchCV
from sklearn import neighbors
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
                ('clf', neighbors.KNeighborsClassifier())])

    k_range = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    algorithm = ['ball_tree', 'kd_tree']
    leaf_size = [15, 30, 60]
    weights = ['uniform', 'distance']

    param_grid = [{'clf__n_neighbors': k_range, 
                   'clf__algorithm': algorithm,
                   'clf__leaf_size': leaf_size,
                   'clf__weights': weights}]

    gs = GridSearchCV(estimator=pipe_svc, 
                    param_grid=param_grid, 
                    scoring='accuracy', 
                    cv=10,
                    n_jobs=-1,
                    verbose = 999)

    gs = gs.fit(X_train, y_train)
    predictions = gs.predict(X_test)
    MSE = np.mean((predictions - y_test)**2)
    #print(gs.best_score_)
    best_params = gs.best_params_
    print(best_params)
    #print('Predicted labels:',predictions)
    #print('True labels:',labels_test)
    print('MSE on the test set:',MSE)

    

if __name__ == "__main__":
    main()