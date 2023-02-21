import clustering.additional_tools as addtools
import clustering.clusters as cl

# optimization for K-Means, MiniBatchKMeans, BisectingKMeans, AggCluWard, BIRCH
def check_value(df_full, alerts_classes, n_clusters, vec_perc, n_neighbors):

    df_full['Outliers'] = addtools.outliers_detection(df_full, n_neighbors=n_neighbors)
    df = df_full.loc[df_full['Outliers'] == 1]
    df = df.drop(['Outliers'], axis=1)
    df = addtools.standarization(df)
    df = addtools.principal_component_analysis(df, vec_perc)

    df_vec = cl.make_kmeans(df, n_clusters=n_clusters, n_jobs=10)
    best_method = "K-Means"
    a = addtools.make_metrics(alerts_classes, df_vec)
    best_value = a
    
    df_vec = cl.make_agglomerative_clustering(df, n_clusters = n_clusters, linkage = 'ward')
    b = addtools.make_metrics(alerts_classes, df_vec)
    if b > best_value:
        best_value = b
        best_method = "AggCluWard"
        

    df_vec = cl.make_bisecting_kmeans(df, n_clusters = n_clusters)
    c = addtools.make_metrics(alerts_classes, df_kmeans)
    if c > best_value:
        best_value = c
        best_method = "BisectingKMeans"
        
    df = cl.make_mini_batch_kmeans(df, n_clusters = n_clusters)
    d = addtools.make_metrics(alerts_classes, df_kmeans)
    if d > best_value:
        best_value = d
        best_method = "MiniBatchKMeans"
        
    df = cl.make_birch(df, n_clusters = n_clusters)
    e = addtools.make_metrics(alerts_classes, df_kmeans)
    if e > best_value:
        best_value = e
        best_method = "BIRCH"
    return best_value, best_method

