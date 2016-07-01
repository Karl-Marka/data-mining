from sklearn.grid_search import GridSearchCV
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pandas as pd

def main():
    data = pd.read_csv('./datasets/train_noduplicate.txt', header = 0, index_col = 0, sep = '\t')
    data = data.T
    labels = pd.read_csv('./datasets/labels_train.txt', sep = '\t', header = None)
    labels = labels.unstack().tolist()

    pipe_svc = Pipeline([('scl', StandardScaler()),
            ('clf', linear_model.LogisticRegression(random_state=5))])

    param_range = [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]

    param_grid = [{'clf__C': param_range, 
               'clf__penalty': ['l1', 'l2']}]

    gs = GridSearchCV(estimator=pipe_svc, 
                      param_grid=param_grid, 
                      scoring='accuracy', 
                      cv=10,
                      n_jobs=-1,
                      verbose = 1)

    gs = gs.fit(data, labels)
    print(gs.best_score_)
    print(gs.best_params_)

if __name__ == "__main__":
    main()