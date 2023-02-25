import pandas as pd
import numpy as np
import sklearn.cluster as sc

# methods finally added

def make_affinity_propagation(DataFrame):
    aff_prop = sc.AffinityPropagation(damping=0.99)
    pred_y = aff_prop.fit_predict(DataFrame)
    return pd.DataFrame({'Groups': pred_y}, index = DataFrame.index)

def make_birch(DataFrame, n_clusters):
    birch = sc.Birch(branching_factor = 50, n_clusters = n_clusters, threshold = 1.5)
    numpy_DataFrame= DataFrame.to_numpy()
    pred_y = birch.fit_predict(numpy_DataFrame.copy(order='C'))
    return pd.DataFrame({'Groups': pred_y}, index = DataFrame.index)

def make_agglomerative_clustering(DataFrame, n_clusters, linkage):
        # for sklearn>=1.4.0
        # cluster = sc.AgglomerativeClustering(n_clusters=n_clusters, metric='euclidean', linkage=linkage)
        # for sklearn>=1.2.0
	cluster = sc.AgglomerativeClustering(n_clusters=n_clusters, affinity='euclidean', linkage=linkage)
	pred_y = cluster.fit_predict(DataFrame)
	return pd.DataFrame({'Groups': pred_y}, index=DataFrame.index)

def make_kmeans(DataFrame, n_clusters):
	kmeans = sc.KMeans(n_clusters=n_clusters, init='random', n_init=10, random_state=0).fit(DataFrame)
	pred_y = kmeans.fit_predict(DataFrame)
	return pd.DataFrame({'Groups': pred_y}, index=DataFrame.index)

def make_mini_batch_kmeans(DataFrame, n_clusters):
	kmeans = sc.MiniBatchKMeans(n_clusters=n_clusters, init='random', n_init=10, random_state=0).fit(DataFrame)
	pred_y = kmeans.fit_predict(DataFrame)
	return pd.DataFrame({'Groups': pred_y}, index=DataFrame.index)

def make_bisecting_kmeans(DataFrame, n_clusters):
	kmeans = sc.BisectingKMeans(n_clusters=n_clusters, n_init=10, bisecting_strategy = "largest_cluster").fit(DataFrame)
	pred_y = kmeans.fit_predict(DataFrame)
	return pd.DataFrame({'Groups': pred_y}, index=DataFrame.index)

def make_spectral_clustering(DataFrame, n_clusters, n_jobs=1):
        numpy_DataFrame = DataFrame.to_numpy()
        spectral = sc.SpectralClustering(n_clusters=n_clusters, n_jobs=n_jobs).fit(numpy_DataFrame)
        pred_y = spectral.fit_predict(numpy_DataFrame)
        return pd.DataFrame({'Groups': pred_y}, index=DataFrame.index)

# methods not used in final project

def make_dbscan(DataFrame, n_jobs=1):
        dbscan = sc.DBSCAN(eps=40.0, min_samples=2, algorithm='ball_tree', metric='minkowski', leaf_size=90, p=2, n_jobs = n_jobs).fit(DataFrame)
        pred_y = dbscan.fit_predict(DataFrame)
        return pd.DataFrame({'Groups': pred_y}, index=DataFrame.index)

def make_affinity_propagation(DataFrame):
	ap = sc.AffinityPropagation().fit(DataFrame)
	pred_y = ap.fit_predict(DataFrame)
	return pd.DataFrame({'Groups': pred_y}, index=DataFrame.index)

def make_mean_shift(DataFrame, n_jobs ):
	ms = sc.MeanShift().fit(DataFrame, n_jobs = n_jobs)
	pred_y = ms.fit_predict(DataFrame)
	return pd.DataFrame({'Groups': pred_y}, index=DataFrame.index)

def make_optics(DataFrame, n_jobs):
	ms = sc.MeanShift().fit(DataFrame, min_cluster_size = 200, n_jobs = n_jobs)
	pred_y = ms.fit_predict(DataFrame)
	return pd.DataFrame({'Groups': pred_y}, index=DataFrame.index)

