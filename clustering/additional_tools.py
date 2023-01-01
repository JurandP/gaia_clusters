import pandas as pd
import json

from sklearn.neighbors import LocalOutlierFactor
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def read_json(filename):
    with open(filename, 'r') as input:
        return json.load(input)

# commented part was previous version of final metric
def make_metrics(df_clusters, df_alerts):
    df = pd.concat([df_clusters, df_alerts], axis = 1, join='inner')
    grouped_by_type = df.groupby(' Class', group_keys=True)
    keys = grouped_by_type.groups.keys()
    metric_value = 0
    #check_is_group_new = []
    for i in keys:
        grouped = grouped_by_type.get_group(i).groupby('Groups').count()
        #if not int(grouped.idxmax()) in check_is_group_new:
            #check_is_group_new.append(int(grouped.idxmax()))
        metric_value += grouped.max()
    
    return float(metric_value)/min(len(df_clusters), len(df_alerts))

def outliers_detection(df, n_neighbors):
    clf=LocalOutlierFactor(n_neighbors=n_neighbors)
    return clf.fit_predict(df)

def principal_component_analysis(df, n_components):
    pca = PCA(svd_solver='full', n_components=n_components)
    principal_components = pca.fit_transform(df)
    return pd.DataFrame(data=principal_components, index=df.index)

def standarization(df):
    scaler = StandardScaler()
    scaler.fit_transform(df)
    X = scaler.transform(df)
    return pd.DataFrame(X, index = df.index)

