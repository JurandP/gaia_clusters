import pandas as pd

import clustering.additional_tools as addtools
import clustering.clusters as cl

#Config
n_neighbors = 10 #number of neighbors in k-neighbors like algorithms
n_clusters = 12 #number of generated clusters
n_jobs = 1 #number processes
vec_perc = 0.85 #coefficient (0,1) how many vectors should be choose in pca algorithm
resultfilename = 'result_tsfresh_3bin_interpolation'
#read data
df_full = pd.read_csv('Final_Database.csv', header = None, index_col=0)
print('Initial dataframe has size ' + str(df_full.shape)+'.')
with open(resultfilename + '.csv', 'w') as input:
    input.write('Initial dataframe has size ' + str(df_full.shape)+'.')
#Outliers removing
df_full['Outliers'] = addtools.outliers_detection(df_full, n_neighbors=n_neighbors)
df = df_full.loc[df_full['Outliers'] == 1]
print('Delete outliers is done.')

df = df.drop(['Outliers'], axis=1)
df = addtools.standarization(df)
print('Data\'s standarization is done.')

df = addtools.principal_component_analysis(df, vec_perc)

print('Principal component analysis is done. Dataframe has size '+str(df.shape)+ '.')
with open(resultfilename + '.csv', 'a') as input:
    input.write('Initial dataframe has size ' + str(df_full.shape)+'.' + '\n')
    input.write('After principal component analysis dataframe has size '+str(df.shape)+ '.' + '\n')
    input.write('Config: vec_perc = ' + str(vec_perc) + ', n_neighbors = '+str(n_neighbors) +
     ', n_clusters = ' + str(n_clusters) + '.')
####################################################
filename = "alerts.csv"

alerts = pd.read_csv(filename, index_col=0)
alerts_classes = alerts[' Class']
alerts_classes = alerts_classes.loc[alerts_classes != 'unknown']

print('POPULATION OF PARTICULAR CLASSES')
print(alerts_classes.groupby(alerts_classes).count())

####################################################
print('Make K-Means')
df_kmeans = cl.make_kmeans(df, n_clusters=n_clusters)
df_results = pd.DataFrame()
df_results['K-Means'] = df_kmeans
print(addtools.make_metrics(alerts_classes, df_kmeans))
with open(resultfilename + '.csv', 'a') as input:
    input.write('\n' + 'K-Means' + '\n' + str(addtools.make_metrics(alerts_classes, df_kmeans)) )
#df_result.drop(columns = ['Groups'])

print('Make DBScan')
df_kmeans = cl.make_dbscan(df, n_jobs=n_jobs)
df_results['DBScan'] = df_kmeans
print(addtools.make_metrics(alerts_classes, df_kmeans))
with open(resultfilename + '.csv', 'a') as input:
    input.write('\n' + 'DBScan' + '\n' + str(addtools.make_metrics(alerts_classes, df_kmeans)) )

print('Make Mini Batch KMeans')
df_kmeans = cl.make_mini_batch_kmeans(df, n_clusters=n_clusters)
df_results['MiniBarchKMeans'] = df_kmeans
print(addtools.make_metrics(alerts_classes, df_kmeans))
with open(resultfilename + '.csv', 'a') as input:
    input.write('\n' + 'Mini Batch KMeans' + '\n' + str(addtools.make_metrics(alerts_classes, df_kmeans)) )

print('Make Bisecting KMeans')
df_kmeans = cl.make_bisecting_kmeans(df, n_clusters=n_clusters)
df_results['BisectingKMeans'] = df_kmeans
print(addtools.make_metrics(alerts_classes, df_kmeans))
with open(resultfilename + '.csv', 'a') as input:
    input.write('\n' + 'Bisecting KMeans' + '\n' + str(addtools.make_metrics(alerts_classes, df_kmeans)) )

print('Make Agglomerative Clustering Avarage')
df_kmeans = cl.make_agglomerative_clustering(df, n_clusters = n_clusters, linkage = 'average')
df_results['AggCluAvarage'] = df_kmeans
print(addtools.make_metrics(alerts_classes, df_kmeans))
with open(resultfilename + '.csv', 'a') as input:
    input.write('\n' + 'Agglomerative Clustering Avarage' + '\n' + str(addtools.make_metrics(alerts_classes, df_kmeans)) )

print('Make Agglomerative Clustering Complete')
df_kmeans = cl.make_agglomerative_clustering(df, n_clusters = n_clusters, linkage = 'complete')
df_results['AggCluComplete'] = df_kmeans
print(addtools.make_metrics(alerts_classes, df_kmeans))
with open(resultfilename + '.csv', 'a') as input:
    input.write('\n' + 'Agglomerative Clustering Complete' + '\n' + str(addtools.make_metrics(alerts_classes, df_kmeans)) )

print('Make Aglomerative Clustering Single')
df_kmeans = cl.make_agglomerative_clustering(df, n_clusters = n_clusters, linkage = 'single')
df_results['AggCluSingle'] = df_kmeans
print(addtools.make_metrics(alerts_classes, df_kmeans))
with open(resultfilename + '.csv', 'a') as input:
    input.write('\n' + 'Agglomerative Clustering Single' + '\n' + str(addtools.make_metrics(alerts_classes, df_kmeans)) )

print('Make Agglomerative Clustering Ward')
df_kmeans = cl.make_agglomerative_clustering(df, n_clusters=n_clusters, linkage='ward')
df_results['AggCluWard'] = df_kmeans
print(addtools.make_metrics(alerts_classes, df_kmeans))
with open(resultfilename +'.csv', 'a') as input:
    input.write('\n' + 'Agglomerative Clustering Ward' + '\n' + str(addtools.make_metrics(alerts_classes, df_kmeans)) )
    input.write('\n' + '\n')

df_results.to_csv(resultfilename + '_dataframe.csv')
