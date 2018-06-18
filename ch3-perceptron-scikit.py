#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 07:15:22 2018

@author: devasenainupakutika
"""

from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap 
import numpy as np

def plot_decision_regions(X, y, classifier, test_idx=None, resolution=0.02):

    # setup marker generator and color map
    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])

    # plot the decision surface
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                         np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    print("Cmap is: ", cmap)
    plt.contourf(xx1, xx2, Z, alpha=0.4, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    # plot class samples
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1],
                    alpha=0.8, c=cmap(idx),
                    marker=markers[idx], label=cl)
    #Highlighting test samples
    if test_idx:
        X_test, y_test = X[test_idx,:], y[test_idx]
        plt.scatter(X_test[:,0],X_test[:,1],c='',alpha=1.0,linewidths=1,marker='o',s=55,label='test set')


iris = datasets.load_iris()
X = iris.data[:,[2,3]] #Only second and third feature columns
y = iris.target

#Splitting the dataset into training and test datasets
#random state is for initial shuffling of training dataset after each epoch
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=0)

#Feature scaling and standardizing features using StandardScaler for optimal performance
sc = StandardScaler() 
sc.fit(X_train) #Estimates sample mean and std deviation for each feature dimension from the training data
X_train_std = sc.transform(X_train) #This then standardises the features using above estimated mean and std
X_test_std = sc.transform(X_test)

#Training perceptron model
ppn = Perceptron(n_iter=40,eta0=0.1, random_state=0)
ppn.fit(X_train_std,y_train)

#Predicting
y_pred = ppn.predict(X_test_std)
print("Misclassified samples: %d" %(y_test != y_pred).sum())

#Classification accuracy
print("Accuracy: %.2f" % accuracy_score(y_test, y_pred)) #y_test are true class labels and y_pred are the predicted class labels

#Plotting Decision Regions with being able to specify the indices of the samples that we want to mark on the resulting plots
X_combined_std = np.vstack((X_train_std,X_test_std))
y_combined = np.hstack((y_train,y_test))
plot_decision_regions(X=X_combined_std, y=y_combined, classifier=ppn,test_idx=range(105,150))
plt.xlabel('Petal length [standardized]')
plt.ylabel('Petal wength [standardized]')
plt.legend(loc='upper left')
plt.show()
