from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np

def main():
    data = pd.read_csv('./datasets/train.txt', header = 0, index_col = 0, sep = '\t')
    if 'Rank' in data.columns:
        del data['Rank']
        print('Deleted Ranks')
    data = data.T
    probes = pd.read_csv('./datasets/probes.txt', header = None, index_col = None, sep = '\t')
    probes = probes.unstack().tolist()
    newdata = pd.DataFrame(data = [])
    for probe in probes:
        if probe in data.columns:
            try:
                newdata[probe] = data[probe]
            except:
                pd.concat([newdata,data[probe]], axis = 1)
    data = newdata
    labels = pd.read_csv('./datasets/labels_train.txt', sep = '\t', header = None)
    labels = labels.unstack().tolist()
    test = pd.read_csv('./datasets/test.txt', header = 0, index_col = 0, sep = '\t')
    if 'Rank' in test.columns:
        del test['Rank']
        print('Deleted Ranks')
    test = test.T
    newtest = pd.DataFrame(data = [])
    for probe in probes:
        if probe in test.columns:
            try:
                newtest[probe] = test[probe]
            except:
                pd.concat([newtest,test[probe]], axis = 1)
    test = newtest
    labels_test = pd.read_csv('./datasets/labels_test.txt', header = None, sep = '\t')
    labels_test = labels_test.unstack().tolist()

    pipe_svc = Pipeline([('scl', StandardScaler()),
                ('clf', RandomForestClassifier(random_state=5))])

    estimators_range = [3,10,100,1000]
    feature_range = [5,10,15,20]
    depth_range = [2, 5, 10, 20, 50]
    split_range = [2,4,6,8]
    leaf_range = [1,2,4,8]

    param_grid = [{'clf__n_estimators': estimators_range,
                   'clf__max_features': feature_range, 
                   'clf__max_depth': depth_range,
                   'clf__min_samples_split': split_range,
                   'clf__min_samples_leaf': leaf_range                    
                   }]

    gs = GridSearchCV(estimator=pipe_svc, 
                    param_grid=param_grid, 
                    scoring='accuracy', 
                    cv=4,
                    n_jobs=-1,
                    verbose=1)

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