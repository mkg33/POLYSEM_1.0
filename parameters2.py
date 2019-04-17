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

data_QU = pd.DataFrame()

data_QU['Duration_before'] = [128.288,71.676,128.501,133.501,97.301,67.574,75.418,84.565,85.688,180.058,70.807,58.472,35.299,68.272,143.232,82.155,137.947,66.197,84.954,118.447,57.088,118.337,125.433,58.203,79.939,89.999,87.192,171.016,82.035,51.399,103.479,76.01,65.951,67.192,141.914,135.103,197.737,81.429,123.075,129.804,93.599,78.218,62.559,94.258,87.604,60.133,63.727,51.152,61.975,84.782,91.638,62.29,61.077,49.154,63.18,56.586,40.059,29.191,54.7,34.985,63.382,52.619,55.688,51.975,105.506,81.848,95.994,59.954,38.622,66.99,69.46,85.665,37.006,59.928,87.574,101.256,71.082,48.008,51.481,76.346,75.403,136.525,59.206,46.107,110.448,68.218,57.739,44.236,54.835,57.035]

data_QU['Duration_after'] = [481.917,281.718,353.259,410.84,777.946,54.555,319.516,183.381,361.612,435.353,98.292,109.13,559.573,59.293,127.992,201.824,114.34,62.627,51.182,71.93,72.619,63.285,112.229,79.984,66.085,91.758,86.017,470.092,52.56,58.308,471.528,60.561,458.789,44.685,105.8, 0,0,0,0,0,0,0,0,0,0,374.306,423.76,387.705,64.251,95.807,368.933,26.816,75.224,61.975,70.89,202.393,125.328,40.531,232.22,55.013,65.418,413.168,233.889,313.5,52.746,91.728,69.52,75.029,83.262,80.5,145.956,61.429,85.852,175.866,83.005,62.29,79.505,51.047,146.076,48.66,56.496,95.059, 0,0,0,0,0,0,0,0]

data_QU['Type'] = [1, 1, 1, 1, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 1, 1, 1, 1, 1,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0]

QU_no_labels = data_QU.drop('Type', axis=1)

QU_no_labels = MinMaxScaler().fit_transform(QU_no_labels)

QU_labels=data_QU['Type']

#data_test_QU = pd.DataFrame()

#data_test_QU['Duration_before'] = [152, 72, 112, 80, 64, 184, 152, 0, 50, 67, 55, 78]

#data_test_QU['Duration_after'] = [315, 537, 1163, 64, 189, 152, 624, 0, 53, 130, 99, 0]

#data_test_QU = MinMaxScaler().fit_transform(data_test_QU)

#QU_labels_test = [1,1,1,1,1,1,1,0,0,0,0,0]

X_train, X_test, y_train, y_test = train_test_split(QU_no_labels, QU_labels, test_size = 0.2)

parameters = {'hidden_layer_sizes': [(4,1,),], 'activation': ['identity', 'logistic', 'tanh', 'relu'], 'solver': ['sgd', 'adam', 'lbfgs'], 'alpha': [0.0001, 0.05], 'learning_rate': ['invscaling', 'constant', 'adaptive'], 'max_iter': [100, 500, 1000],}

clf = GridSearchCV(mlp, parameters, n_jobs=-1, cv=3)

clf.fit(X_train, y_train)

print(clf.best_params_)

print(clf.cv_results_['mean_test_score'])

print(clf.cv_results_['std_test_score'])

QU_prediction = clf.predict(X_test)

print('Results on the test set: ')

print(classification_report(y_test, QU_prediction))

print(y_test)

print(QU_prediction)
