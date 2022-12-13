import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn import metrics
from clustering.additional_tools import read_json

classes_labels = ['AGN', 'BL Lac', 'CV', 'QSO', 'SN II', 'SN IIn', 'SN Ia', 'YSO']
methods = ['DBSCAN', 'K-Means', 'MiniBatchKMeans', 'BisectingKMeans', 'AggCluAvarage', 'AggCluWard', 'AggCluSingle']

def label_funct(name):
    i = 0
    for j in classes_labels:
        i+=1
        if name == j:
            return i 
    return 0

config = read_json('configs/config.json')
df = pd.read_csv(config['result_name'] + '_dataframe.csv')
df['class_label'] = df[' Class'].apply(label_funct)
df = df.loc[df['class_label'] != 0]

print(df)

for i in methods:
    confusion_matrix = metrics.confusion_matrix(df['class_label'], df[i])
    cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix)
    cm_display.plot()
    plt.title(i)
    plt.savefig('ConfusionMatrixPNG/' + i)
