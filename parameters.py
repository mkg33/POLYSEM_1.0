#!/usr/bin/python3

# coding: utf-8

# Copyright (c) 2018 Maja Gwozdz. Version 1.0. Latest release: 06-05-2018
# Distributed under the MIT license.


from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

import pandas as pd

mlp = MLPClassifier()

data_rel = pd.DataFrame()

data_rel['Duration_before']=[110.42,35.778,66.593,51.377,0,57.215,318.858,370.123,25.094,126.69,50.299,83,308.649,25.497,0,73.173,108.322,0,31.287,175.417,0,0,185.237,31.571,97.252,40.334,92.065,0,0,114.115,233.994,236.786,57.499,0,111.81,79.501,0,51.272,210.858,116.172,111.705,89.675,124.239,157.43,0,205.506,68.629,164.257,87.708,159.511,61.293,41.431,98.157,0,56.795,170.514,48.353,80.803,51.842,17.117,119.475,0,0,262.212,81.743,13.49,0,0,25.096,49.273,67.539,21.383,137.349,0,0,0,0,30.583,0,27.148,0,33.065,56.324,33.663,149.886,0,0,0,34.131,0,0,0,55.373,0,0,0,0,0,109.49,0,0,91.466,0,0,0,0,0,0,77.655,91.351,0,0,0,0,0,0,0,0,0,0,0,0,0,0,93.779,41.636,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

data_rel['Duration_after'] = [50.995,90.953,118.322,0,0,111.069,84.879,277.815,0,316.111,104.684,76.526,235.319,388.513,382.696,0,95.095,89.909,99.699,78.749,50.903,91.481,126.331,0,0,141.555,0,177.094,348.352,80.411,125.432,42.112,77.724,155.387,450.534,77.806,377.457,49.722,185.349,84.49,0,0,492.771,100.261,0,0,96.556,0,83.622,66.302,434.5,417.119,0,110.04,120.635,438.826,461.495,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,17.734,0,272.691,0,0,0,0,208.681,0,0,64.228,48.188,0,0,0,0,0,56.623,70.337,0,0,0,40.643,52.335,49.527,79.501,29.551,0,53.188,46.452,24.658,120.34,60.179,81.016,0,0,0,0,0,0,83.651,0,0,0,0,69.572,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

data_rel['Type'] = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

rel_no_labels = data_rel.drop('Type', axis=1)

rel_no_labels = MinMaxScaler().fit_transform(rel_no_labels)

rel_labels=data_rel['Type']

X_train, X_test, y_train, y_test = train_test_split(rel_no_labels, rel_labels, test_size = 0.2)


#data_test_rel['Duration_after']=[424, 0.000, 88.000, 0.000, 408, 0.000, 72, 136, 0.000, 0.000]

#data_test_rel = MinMaxScaler().fit_transform(data_test_rel)

#rel_labels_test = [1,0,1,0,1,0,1,1,0,0]

parameters = {'hidden_layer_sizes': [(1,)], 'activation': ['identity', 'relu', 'tanh', 'logistic'], 'solver': ['sgd', 'adam', 'lbfgs'], 'alpha': [0.0001, 0.05], 'learning_rate': ['invscaling', 'constant', 'adaptive'], 'max_iter': [100, 500, 1000],}

clf = GridSearchCV(mlp, parameters, n_jobs=-1, cv=3)

clf.fit(X_train, y_train)

print(clf.best_params_)

print(clf.cv_results_['mean_test_score'])

print(clf.cv_results_['std_test_score'])

rel_prediction = clf.predict(X_test)

print('Results on the test set: ')

print(classification_report(y_test, rel_prediction))

print(y_test)

print(rel_prediction)
