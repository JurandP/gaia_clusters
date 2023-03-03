import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt
import clustering.additional_tools as addtools
import clustering.clusters as cl
import os

from sklearn import metrics
from clustering.additional_tools import read_json

def prepare_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--suffix_name", type=str,
            help="Suffix of final database's name in Final_Database_* format." )
    parser.add_argument("-j", "--n_jobs", type=int,
        help="Number of processes used to clustering. Default --n_jobs = 1", default=1)
    parser.add_argument("-c", "--n_clusters", type=int,
    	help="Number of clusters to choose in kmeans methods. \
    	Default --n_clusters = 8", default=8)
    parser.add_argument("-e", "--n_neighbors", type=int,
    	help="Number of n neighbors used in removing outliers \
    	process and clustering methods with n neighbors parameter. \
    	Default --n_neighbors = 10", default=10)
    parser.add_argument("-v", "--vec_perc", type=float,
    	help="Percent of principal components after PCA. Input in (0,1) range. \
    	Default --vec_perc = 0.95", default=0.95)
    return parser.parse_args()


def main():
    args = prepare_argparse()
    
    suffix_name = args.suffix_name
    n_clusters = args.n_clusters
    n_neighbors = args.n_neighbors
    n_jobs = args.n_jobs
    vec_perc = args.vec_perc
    
    # Data directory
    out_dir = 'Data/'
    
	# Read database
    df_full = pd.read_csv(out_dir + 'Final_Database_' + suffix_name + '.csv', header = None, index_col=0)
    print('Initial dataframe has size ' + str(df_full.shape)+'.')
	
    with open(out_dir + 'result_' + suffix_name + '.csv', 'w') as input:
        input.write('Initial dataframe has size ' + str(df_full.shape)+'.')
	
    # Outliers removing
    df_full['Outliers'] = addtools.outliers_detection(df_full, n_neighbors=n_neighbors)
    df = df_full.loc[df_full['Outliers'] == 1]
    print('Delete outliers is done.')

    df = df.drop(['Outliers'], axis=1)
    df = addtools.standarization(df)
    print('Data\'s standarization is done.')

    # PCA
    df = addtools.principal_component_analysis(df, vec_perc)
    print('Principal component analysis is done. Dataframe has size '+str(df.shape)+ '.')
    
    with open(out_dir + 'result_' + suffix_name + '.csv', 'a') as input:
        input.write('Initial dataframe has size ' + str(df_full.shape)+'.' + '\n')
        input.write('After principal component analysis dataframe has size '+str(df.shape)+ '.' + '\n')
        input.write('Config: vec_perc = ' + str(vec_perc) + ', n_neighbors = '+str(n_neighbors) +
        ', n_clusters = ' + str(n_clusters) + '.')

    # Read alerts list   
    alerts = pd.read_csv('alerts.csv', index_col=0)
	
    # Partition of alerts by classes
    alerts_classes = alerts[' Class']
    alerts_classes = alerts_classes.loc[alerts_classes != 'unknown']
    to_print = alerts_classes.groupby(alerts_classes).count()
    print('Plurality of biggest groups by classes index: \n')
    print(to_print.loc[to_print > 100])
	
    print(alerts_classes)
    df_results = pd.DataFrame()

    print('Make BIRCH')
    df_birch = cl.make_birch(df, n_clusters = n_clusters)
    df_results['BIRCH'] = df_birch
    metric = addtools.make_metrics(alerts_classes, df_birch)
    print(metric)
    with open(out_dir + 'result_' + suffix_name + '.csv', 'a') as input:
        input.write('\n' + 'BIRCH' + '\n' + str(metric))

    print('Make K-Means')
    df_kmeans = cl.make_kmeans(df, n_clusters=n_clusters)
    df_results['K-Means'] = df_kmeans
    metric = addtools.make_metrics(alerts_classes, df_kmeans)
    print(metric)
    with open(out_dir + 'result_' + suffix_name + '.csv', 'a') as input:
        input.write('\n' + 'K-Means' + '\n' + str(metric) )

    print('Make Mini Batch KMeans')
    df_kmeans = cl.make_mini_batch_kmeans(df, n_clusters=n_clusters)
    df_results['MiniBatchKMeans'] = df_kmeans
    print(addtools.make_metrics(alerts_classes, df_kmeans))
    with open(out_dir + 'result_' + suffix_name + '.csv', 'a') as input:
        input.write('\n' + 'Mini Batch KMeans' + '\n' + str(metric) )

    print('Make Bisecting KMeans')
    df_kmeans = cl.make_bisecting_kmeans(df, n_clusters=n_clusters)
    df_results['BisectingKMeans'] = df_kmeans
    print(addtools.make_metrics(alerts_classes, df_kmeans))
    with open(out_dir + 'result_' + suffix_name + '.csv', 'a') as input:
        input.write('\n' + 'Bisecting KMeans' + '\n' + str(addtools.make_metrics(alerts_classes, df_kmeans)) )

    print('Make Agglomerative Clustering Ward')
    df_ward = cl.make_agglomerative_clustering(df, n_clusters=n_clusters, linkage='ward')
    df_results['AggCluWard'] = df_ward
    print(addtools.make_metrics(alerts_classes, df_ward))
    with open(out_dir + 'result_' + suffix_name + '.csv', 'a') as input:
        input.write('\n' + 'Agglomerative Clustering Ward' + '\n' + str(addtools.make_metrics(alerts_classes, df_kmeans)) )
        input.write('\n \n')

    df_results = pd.concat([df_results, alerts[' Class']], axis=1).reindex(df_results.index)
    df_results.to_csv(out_dir + 'result_' + suffix_name + '_dataframe.csv')
	
    classes_labels = ['AGN', 'BL Lac', 'CV', 'QSO', 'SN II', 'SN IIn', 'SN Ia', 'YSO']
    methods = ['K-Means', 'MiniBatchKMeans', 'BisectingKMeans', 'AggCluWard', 'BIRCH']

    def label_funct(name):
        i = -1
        for j in classes_labels:
            i+=1
            if name == j:
                return i 
        return 0

	# prepare class_label column to print confusion matrices
    df_results['class_label'] = df_results[' Class'].apply(label_funct)
	# df_results = df_results.loc[df_results['class_label'] != 0]

	# print confusion matrices
    if not os.path.isdir(out_dir + 'ConfusionMatricesPNG/'):
        os.mkdir(out_dir + 'ConfusionMatricesPNG/')
		
    if not  os.path.isdir(out_dir + 'ConfusionMatricesPNG/' + 'results_' + suffix_name):
        os.mkdir(out_dir + 'ConfusionMatricesPNG/' + 'results_' + suffix_name)


    for i in methods:
        confusion_matrix = metrics.confusion_matrix(df_results['class_label'], df_results[i], labels=range(n_clusters))
        cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix)
        cm_display.plot()
        plt.title(i)
        plt.savefig(out_dir + 'ConfusionMatricesPNG/' + 'results_' + suffix_name + '/' + i)


if __name__ == '__main__':
    main()
