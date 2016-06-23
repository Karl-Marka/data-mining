print('Loading libraries')
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import decomposition
from mpl_toolkits.mplot3d import Axes3D
from sklearn.externals import joblib

print('Reading data')
train = pd.read_csv('Illumina_F15.txt', sep = '\t', header = 0, index_col = 0)
train = train.T
pca = joblib.load('./PCA_model_F15/PCA.pkl') 
pca.fit(train)
X_pca = pca.transform(train)

def closeFunc():
    print('''Type 'quit' and press enter to exit program''')
    answer = input(': ')
    if answer == 'quit':
        quit()
    else:
        closeFunc()

def main():
    q = input('How many dimensions do you want plotted? (0 = all): ')    
    try:
        q = int(q)
        if q == 0:
            dimensions = len(train)
            first = round(dimensions/3)
            second = 2*first
            plotter(first, second, dimensions)
        elif q < 3:
            print('Must be more than three!')
            main()
        elif q <= len(train):
            dimensions = q
            first = round(dimensions/3)
            second = 2*first
            plotter(first, second, dimensions)        
        else:
            print('Must be less than or equal to the number of dimensions!')
            main()
    except:
        print('Must be an integer!')
        main()

def plotter(first, second, dimensions):
    dimensions = dimensions + 1
    for i in range(0,first):
        for j in range(first,second):
            for g in range(second,dimensions):
                fig = plt.figure(figsize=(10, 8), dpi=80)
                ax = fig.add_subplot(111, projection='3d')
                print('Processing components:',str(i),str(j),str(g))
                ax.scatter(X_pca[0:40, i], X_pca[0:40, j], X_pca[0:40, g], s=90, c = 'cyan', depthshade=True, linewidths=0, label = 'Healthy')
                ax.scatter(X_pca[41:71, i], X_pca[41:71, j], X_pca[41:71, g], s=90, c = 'blue', depthshade=True, linewidths=0, label = 'Idiopathic PAH')
                ax.scatter(X_pca[72:114, i], X_pca[72:114, j], X_pca[72:114, g], s=90, c = 'red', depthshade=True, linewidths=0, label = 'Ssc PAH')
                ax.scatter(X_pca[115:134, i], X_pca[115:134, j], X_pca[115:134, g], s=90, c = 'magenta', depthshade=True, linewidths=0, label = 'Ssc without PAH')
                ax.scatter(X_pca[135:143, i], X_pca[135:143, j], X_pca[135:143, g], s=90, c = 'orange', depthshade=True, linewidths=0, label = 'Interstitial LD')
                ax.legend(loc = 'upper right')
                filename = './plots/plot_components_' + str(i) + '_' + str(j) + '_' + str(g) + '.png'
                fig.savefig(filename)
                fig = None
                ax = None
    closeFunc()

if __name__ == "__main__":
    main()