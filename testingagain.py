import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.svm import  SVC
import numpy as np
from sklearn.metrics import accuracy_score
 
# Load the breast cancer dataset

bc = datasets.load_iris()
# print(bc.target)
df = pd.DataFrame(data=bc.data)
df["label"] = bc.target
df.info() 

plt.scatter(df[0][df["label"] == 0], df[1][df["label"] == 0],
            color='red', marker='o', label='Setosa')
plt.scatter(df[0][df["label"] == 1], df[1][df["label"] == 1],
            color='green', marker='*', label='Versicolor')
plt.scatter(df[0][df["label"] == 2], df[1][df["label"] == 2],
            color='blue', marker='*', label='Virginica')

plt.xlabel('Sepal Length')
plt.ylabel('Petal length')
plt.legend(loc='upper left')
plt.show()

X=df.iloc[:,0:2]
y=df['label']
svm = SVC(kernel='rbf', random_state=1, gamma= "auto", C=3)

#train the model
svm.fit(X, y)
SVC(C=10, gamma=0.001, random_state=1)
def plot_contours(ax, clf, xx, yy, **params):
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    out = ax.contourf(xx, yy, Z, **params)
    return out

def make_meshgrid(x, y, h=.02):
    x_min, x_max = x.min() - 1, x.max() + 1
    y_min, y_max = y.min() - 1, y.max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    return xx, yy

fig, ax = plt.subplots()
# title for the plots
title = ('Decision surface of SVC ')
# Set-up grid for plotting.
X0, X1 = X.iloc[:, 0], X.iloc[:, 1]
xx, yy = make_meshgrid(X0, X1)

plot_contours(ax, svm, xx, yy, cmap=plt.cm.YlGn, alpha=0.8)
ax.scatter(X0, X1, c=y, cmap=plt.cm.coolwarm, s=50, alpha=0.7 )
ax.set_xlabel('Petal Length')
ax.set_ylabel('Setal Length')
ax.set_xticks(())
ax.set_yticks(())
ax.set_title(title)
plt.show()

#Conclusion there are 3 type of iris in the graph, they are Setosa Versicolor Virginica. In this graph we classify 3 types based on the petal and setal length. And finally we can say that some variant has unique length. for example a semicolor can have a sepal length of virginica and petal length of setosa. However it is still consider semicolor