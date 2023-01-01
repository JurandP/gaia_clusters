import clustering.additional_tools as addtools
import clustering.clusters as cl

# optimization for DBSCAN, AggAverage, AggSingle, AggWard, AggComplete
def check_value(df_full, alerts_classes, n_clusters, vec_perc, n_neighbors):

    df_full['Outliers'] = addtools.outliers_detection(df_full, n_neighbors=n_neighbors)
    df = df_full.loc[df_full['Outliers'] == 1]
    df = df.drop(['Outliers'], axis=1)
    df = addtools.standarization(df)
    df = addtools.principal_component_analysis(df, vec_perc)

    df_kmeans = cl.make_dbscan(df, n_jobs=10)
    best_method = "DBScan"

    a = addtools.make_metrics(alerts_classes, df_kmeans)
    best_value = a
    df_kmeans = cl.make_agglomerative_clustering(df, n_clusters = n_clusters, linkage = 'average')

    b = addtools.make_metrics(alerts_classes, df_kmeans)
    if b > best_value:
        best_value = b
        best_method = "agglomerative_clustering_average"
    df_kmeans = cl.make_agglomerative_clustering(df, n_clusters = n_clusters, linkage = 'single')

    c = addtools.make_metrics(alerts_classes, df_kmeans)
    if c > best_value:
        best_value = c
        best_method = "agglomerative_clustering_single"
    df_kmeans = cl.make_agglomerative_clustering(df, n_clusters = n_clusters, linkage = 'ward')

    d = addtools.make_metrics(alerts_classes, df_kmeans)
    if d > best_value:
        best_value = d
        best_method = "agglomerative_clustering_ward"
    df_kmeans = cl.make_agglomerative_clustering(df, n_clusters = n_clusters, linkage = 'complete')

    e = addtools.make_metrics(alerts_classes, df_kmeans)
    if e > best_value:
        best_value = e
        best_method = "agglomerative_clustering_complete"
    return best_value, best_method

