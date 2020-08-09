import math

import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.naive_bayes import CategoricalNB
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestClassifier

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
    #Sepak poarno bilo so seaborn barplot, ama dolgo vreme trae za sekoja kolona da napravi plot
    plt.figure()
    sns.barplot(data_x,data_y)
    plt.show()

def statisticalInfo(data:pd.DataFrame):
    corr_matrix = data.corr()

    sns.heatmap(corr_matrix)
    plt.title("Heatmap of the correlation between columns")
    plt.show()

    column_names = list(data.columns)[:-1]
    column_names.remove("ARR_DEL15")
    data_y = data["ARR_DEL15"]

    for c in column_names:
        data_x = data[c]
        barPlot(data_x,data_y)

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

def getSampleDataset(dataset):
    for row in dataset:
        row[6] = int(row[6])

    return dataset

def getTrainingSet(fullData):
    trainingSet = fullData['January'].values.tolist()+fullData['February'].values.tolist()+fullData['March'].values.tolist()
    trainingSet = getDataset(trainingSet)
    return trainingSet

def getTestingSet(fullData):
    testingSet = fullData['April'].values.tolist()
    testingSet = getDataset(testingSet)
    return testingSet


def randomForestClassification(X, Y, test_set_x, test_set_y):
    max_depths = [3,5,8,12]
    n_estimators = [10, 30, 50, 80, 100]
    y_estimators = dict()
    y_estimators["gini"] = []
    y_estimators["entropy"] = []
    for n in n_estimators:
        rf_g = RandomForestClassifier(n,"gini")
        rf_e = RandomForestClassifier(n,"entropy")
        rf_g.fit(X,Y)
        rf_e.fit(X, Y)
        predictions = rf_g.predict(test_set_x)
        #Zemam f1 score bidejki zema vo predvid i promashenite klasifikacii
        y_estimators["gini"].append(f1_score(test_set_y,predictions))
        predictions = rf_e.predict(test_set_x)
        y_estimators["entropy"].append(f1_score(test_set_y, predictions))
        print("Finished prediction for no. of estimators",n)
    plt.figure()
    plt.title("F1 score measured by no. of estimators")
    plt.xlabel("No. of estimators")
    plt.ylabel("F1 Score")
    g_plot, = plt.plot(n_estimators,y_estimators["gini"],color="r")
    e_plot, = plt.plot(n_estimators,y_estimators["entropy"],color="b")
    plt.legend([g_plot,e_plot],["Gini","Entropy"])
    plt.show()

    #Posho se gleda deka so 100 estimatori bez ogranichuvanje na dlabochinata dava najdobar rezultat, zemame 100 za
    #broj na estimatori za slednava proverka
    y_depths = dict()
    y_depths["gini"] = []
    y_depths["entropy"] = []
    for depth in max_depths:

        rf_g = RandomForestClassifier(n_estimators=100, criterion="gini",max_depth=depth)
        rf_e = RandomForestClassifier(n_estimators=100, criterion="entropy",max_depth=depth)
        rf_g.fit(X, Y)
        rf_e.fit(X, Y)
        predictions = rf_g.predict(test_set_x)
        # Zemam f1 score bidejki zema vo predvid i promashenite klasifikacii
        y_depths["gini"].append(f1_score(test_set_y, predictions))
        predictions = rf_e.predict(test_set_x)
        y_depths["entropy"].append(f1_score(test_set_y, predictions))
        print("Finished prediction for depth", depth)

    plt.figure()
    plt.title("F1 score measured by max depth")
    plt.xlabel("Max Depth")
    plt.ylabel("F1 Score")
    g_plot, = plt.plot(max_depths, y_depths["gini"], color="r")
    e_plot, = plt.plot(max_depths, y_depths["entropy"], color="b")
    plt.legend([g_plot, e_plot], ["Gini", "Entropy"])
    plt.show()



if __name__ == '__main__':
    full_data = readFullData()

    # statisticalInfo(pd.concat(full_data.values()))
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

    test_set_x = encoder.transform([row[:-1] for row in testingSet])

    test_set_y = [row[-1] for row in testingSet]
    predictions = classifier.predict(test_set_x)

    right = 0

    for y, prediction in zip(test_set_y, predictions):
        if y == prediction:
            right += 1

    accuracy = right/len(testingSet)
    print(accuracy)
    print(f1_score(test_set_y,predictions))

    # randomForestClassification(X,Y,test_set_x,test_set_y)

    #Predviduvanje na zadocnuvanje so test primeroci
    test_primeroci = pd.read_csv("Sample.csv").values.tolist()
    test_primeroci = getSampleDataset(test_primeroci)
    encoder.fit(test_primeroci)
    test_primeroci = encoder.transform(test_primeroci)

    RFClassifier = RandomForestClassifier()
    RFClassifier.fit(X,Y)
    print("\nPredviduvanje na zadocnuvanje kaj test primerocite:\n")
    print("Predviduvanje spored Naive Bayes:",classifier.predict(test_primeroci))
    print("Predviduvanje spored Random Forest:", RFClassifier.predict(test_primeroci))

