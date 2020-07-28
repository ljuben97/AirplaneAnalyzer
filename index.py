import math

import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.naive_bayes import CategoricalNB
from sklearn.preprocessing import OrdinalEncoder


def readFullData():
    #Podatocite se smestuvaat vo tn. hash mappa (dict vo python) so vrednost na kluchot po imeto na mesecot
    data_frames =dict()

    data_frames["January"] = pd.read_csv("January.csv")
    data_frames["February"] = pd.read_csv("February.csv")
    data_frames["March"] = pd.read_csv("March.csv")
    data_frames["April"] = pd.read_csv("April.csv")
    #Za da gi spoish site podatoci posle imash funkcija pd.concat, ama taa zima lista od Dataframeovi
    return data_frames


def barPlot(data_x, data_y):
    plt.figure()
    plt.bar(data_x,data_y)
    plt.show()
    # unique_x_values = set(data_x.to_numpy())
    # uniq_x_val_count = []
    # for val in unique_x_values:


def statisticalInfo(data:pd.DataFrame,target_column_name):
    corr_matrix = data.corr()

    sns.heatmap(corr_matrix)
    plt.title("Heatmap of the correlation between columns")
    plt.show()

    column_names = data.columns[:-1]
    data_y = data[target_column_name]
    # Malce podolgo kje trae za barplot ama ne mi se svigja kako gi pretstavuva taka da kje probam rachno ubavo
    # da go napravam
    # for c in column_names:
    #     data_x = data[c]
    #     barPlot(data_x,data_y)

def getDataset(dataset):
    dataset = [row[:-1] for row in dataset]
    for row in dataset:
        if math.isnan(row[6]):
            row[6] = 0.0
        if math.isnan(row[7]):
            row[7] = 0.0
        row[6] = int(row[6])
        row[7] = int(row[7])
        temp = row[7]
        row[7] = row[8]
        row[8] = temp
    return dataset

def getTrainingSet(fullData):
    trainingSet = fullData['January'].values.tolist()+fullData['February'].values.tolist()+fullData['March'].values.tolist()
    trainingSet = getDataset(trainingSet)
    return trainingSet

def getTestingSet(fullData):
    testingSet = fullData['March'].values.tolist()
    testingSet = getDataset(testingSet)
    return testingSet

if __name__ == '__main__':
    full_data = readFullData()
    #pd.concat(full_data.values()) #ti e ustvari spojuvanjeto na site podatoci
    #statisticalInfo(pd.concat(full_data.values()),'ARR_DEL15')
    trainingSet = getTrainingSet(full_data)
    testingSet = getTestingSet(full_data)
    dataset = trainingSet + testingSet

    classifier = CategoricalNB()
    encoder = OrdinalEncoder()
    encoder.fit([row[:-1] for row in dataset])

    X = [row[:-1] for row in trainingSet]
    X = encoder.transform(X)
    Y = [row[-1] for row in trainingSet]

    classifier.fit(X, Y)

    test_set_x = encoder.transform(row[:-1] for row in testingSet)
    test_set_y = [row[-1] for row in testingSet]
    predictions = classifier.predict(test_set_x)

    right = 0

    for y, prediction in zip(test_set_y, predictions):
        if y == prediction:
            right += 1

    accuracy = right/len(testingSet)
    print(accuracy)

