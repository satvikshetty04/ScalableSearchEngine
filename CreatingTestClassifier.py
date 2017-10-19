import json
import collections
import pandas as pd
import glob
import sys
from sklearn.multiclass import OneVsRestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.linear_model import SGDClassifier
from sklearn.externals import joblib
import numpy as np
import random
import datetime

random.seed(100)
start_time = datetime.datetime.now()

# ---------------------- Reading Json file for Test data

with open('Test//TestData.json', 'r') as content_file:
    json_data = content_file.read()
py_object_test_data = json.loads(json_data, object_pairs_hook=collections.OrderedDict)['TestData']
test_data_x = []

for key, value in py_object_test_data.items():
    test_data_x.append(value["bodyText"])


# ---------------------- Reading Prediction Labels

labels = []
with open('Test//topicDictionary.txt', 'r') as content_file:
    labels = content_file.read().split("\n")
print(labels)

# ---------------------- Reading & Cleaning the Json file for Training set

print("Reading the input data...")
files = glob.glob("*.json")
data = dict
flag = 0
train_data_x = []
train_data_y = []
unique_train_labels = set()

for file in files[28:]:
    with open(file, 'r') as content_file:
        json_data = content_file.read()
    py_object_train_data = json.loads(json_data, object_pairs_hook=collections.OrderedDict)['TrainingData']

    print("File " + str(flag + 1))
    flag += 1

    for key, value in py_object_train_data.items():
        if value["topics"] and value["bodyText"] != "":
            temp = []
            for each_label in value["topics"]:
                if each_label in labels:
                    temp.append(each_label)
            if temp:
                unique_train_labels.update(temp)
                train_data_x.append(value["bodyText"])
                train_data_y.append(temp)
    print(len(train_data_x))
    print(len(train_data_y))
    del py_object_train_data
    del json_data

print("Number of unique labels in Training set:")
print(len(unique_train_labels))
print("*"*10)

# ---------------------- Determining labels for which there exists no train data
non_existent = list(set(labels).difference(unique_train_labels))
print(non_existent)


# ---------------------- Generate vectors for words in training data Articles
print("Generating frequency vectors for the words present in the training set. This will take a while...")
#
vectorizer = TfidfVectorizer(min_df=0.005, max_df=0.90, stop_words='english',  smooth_idf=True,
                             norm="l2", sublinear_tf=False, use_idf=True, ngram_range=(1, 3))
X = vectorizer.fit_transform(train_data_x)

# ---------------------- Generate vectors for words in test data Articles
xTest = vectorizer.transform(test_data_x)

# ---------------------- Level binarizer for Class variable of Train set
print("Converting the class variable to binary matrix...")
mlb_train = MultiLabelBinarizer(classes = labels)
print(mlb_train)
train_data_y = mlb_train.fit_transform(train_data_y)
print(train_data_y)
print(len(train_data_y[1]))

# ---------------------- Fitting a One Vs Rest Classifier using the Naive Bayes classifier
print("Training the model...")
classifier = OneVsRestClassifier(SGDClassifier(alpha=0.0001, learning_rate="optimal",
                                               class_weight="balanced", n_iter=100, n_jobs=-1)).fit(X, train_data_y)

# ---------------------- Saving model
joblib.dump(classifier, 'SGDClassifier.pkl')

print("Time taken: " + str(datetime.datetime.now() - start_time))