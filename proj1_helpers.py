# -*- coding: utf-8 -*-
"""some helper functions for project 1."""
import csv
import numpy as np


def load_csv_data(data_path, sub_sample=False):
    """Loads data and returns y (class labels), tX (features) and ids (event ids)"""
    y = np.genfromtxt(data_path, delimiter=",", skip_header=1, dtype=str, usecols=1)
    x = np.genfromtxt(data_path, delimiter=",", skip_header=1)
    ids = x[:, 0].astype(np.int)
    input_data = x[:, 2:]

    # convert class labels from strings to binary (-1,1)
    yb = np.ones(len(y))
    yb[np.where(y=='b')] = -1
    
    # sub-sample
    if sub_sample:
        yb = yb[::50]
        input_data = input_data[::50]
        ids = ids[::50]

    return yb, input_data, ids


def predict_labels(weights, data):
    """Generates class predictions given weights, and a test data matrix"""
    y_pred = np.dot(data, weights)
    y_pred[np.where(y_pred <= 0)] = -1
    y_pred[np.where(y_pred > 0)] = 1
    
    return y_pred


def create_csv_submission(ids, y_pred, name):
    """
    Creates an output file in csv format for submission to kaggle
    Arguments: ids (event ids associated with each prediction)
               y_pred (predicted class labels)
               name (string name of .csv output file to be created)
    """
    with open(name, 'w') as csvfile:
        fieldnames = ['Id', 'Prediction']
        writer = csv.DictWriter(csvfile, delimiter=",", fieldnames=fieldnames)
        writer.writeheader()
        for r1, r2 in zip(ids, y_pred):
            writer.writerow({'Id':int(r1),'Prediction':int(r2)})


#####################################
###                               ###
#####################################

def predict_labels_logistic(w , testF):
    '''Changed version of predict labels function to account for the fact
    that logistic regression outputs answers between 0 and 1 and not -1 and 1'''
    y_pred = 1 / (1 + np.exp(- np.dot(testF, w)))  # prediction of the logistic function
    y_pred[np.where(y_pred <= 0.5)] = -1
    y_pred[np.where(y_pred > 0.5)] = 1
    return y_pred

def get_accuracy_logistic( w , testY , testF ):
    
    y_pred = predict_labels_logistic( w , testF )
    unique, counts = np.unique((y_pred == testY) , return_counts=True)
    res = dict(zip(unique, counts)) 

    return res[True]/(res[True]+res[False])


def get_accuracy( w , testY , testF ):
    
    y_pred = predict_labels( w , testF )
    unique, counts = np.unique((y_pred == testY) , return_counts=True)
    res = dict(zip(unique, counts)) 

    return res[True]/(res[True]+res[False])


def acc_f1(weights, data, ytest):
    y_pred = predict_labels(weights, data)
    ytest = (ytest + 1) / 2
    y_sum = y_pred + ytest  # adds true and predicted values
    tp = list(y_sum).count(2)  # true positives
    fp = list(y_sum).count(1)  # false positives
    tn = list(y_sum).count(-1)  # true negatives
    fn = list(y_sum).count(0)  # false negatives
    acc = 100 * (tp + tn) / (tp + fp + tn + fn)
    tpr = 100 * (tp) / (tp + fn)
    tnr = 100 * (tn) / (tn + fp)
    ppv = 100 * (tp) / (tp + fp)
    f1 = 2 * (tpr * ppv) / (tpr + ppv)
    return acc, f1