import pandas as pd
import sklearn.cluster as sc

#AGGLOMERATIVE
def make_agglomerative_clustering(DataFrame, n_clusters, linkage):
	cluster = sc.AgglomerativeClustering(n_clusters=n_clusters, affinity='euclidean', linkage=linkage)
	pred_y = cluster.fit_predict(DataFrame)
	return pd.DataFrame({'Groups': pred_y}, index=DataFrame.index)

def make_kmeans(DataFrame, n_clusters):
	kmeans = sc.KMeans(n_clusters=n_clusters, init='random', random_state=0).fit(DataFrame)
	pred_y = kmeans.fit_predict(DataFrame)
	return pd.DataFrame({'Groups': pred_y}, index=DataFrame.index)

def make_spectral_clustering(DataFrame, n_clusters, n_jobs=1):
	spectral = sc.SpectralClustering(n_clusters=n_clusters, n_jobs = n_jobs).fit(DataFrame)
	pred_y = spectral.fit_predict(DataFrame)
	return pd.DataFrame({'Groups': pred_y}, index=DataFrame.index)

def make_dbscan(DataFrame, n_jobs=1):
	dbscan = sc.DBSCAN(eps=40.0, min_samples=2, algorithm='ball_tree', metric='minkowski', leaf_size=90, p=2, n_jobs = n_jobs).fit(DataFrame)
	pred_y = dbscan.fit_predict(DataFrame)
	return pd.DataFrame({'Groups': pred_y}, index=DataFrame.index)

def make_affinity_propagation(DataFrame):
	ap = sc.AffinityPropagation().fit(DataFrame)
	pred_y = ap.fit_predict(DataFrame)
	return pd.DataFrame({'Groups': pred_y}, index=DataFrame.index)

def make_mini_batch_kmeans(DataFrame, n_clusters):
	kmeans = sc.MiniBatchKMeans(n_clusters=n_clusters, init='random', random_state=0).fit(DataFrame)
	pred_y = kmeans.fit_predict(DataFrame)
	return pd.DataFrame({'Groups': pred_y}, index=DataFrame.index)

def make_mean_shift(DataFrame, n_jobs ):
	ms = sc.MeanShift().fit(DataFrame, n_jobs = n_jobs)
	pred_y = ms.fit_predict(DataFrame)
	return pd.DataFrame({'Groups': pred_y}, index=DataFrame.index)

def make_bisecting_kmeans(DataFrame, n_clusters):
	kmeans = sc.BisectingKMeans(n_clusters=n_clusters, bisecting_strategy = "largest_cluster").fit(DataFrame)
	pred_y = kmeans.fit_predict(DataFrame)
	return pd.DataFrame({'Groups': pred_y}, index=DataFrame.index)

def make_optics(DataFrame, n_jobs):
	ms = sc.MeanShift().fit(DataFrame, min_cluster_size = 200, n_jobs = n_jobs)
	pred_y = ms.fit_predict(DataFrame)
	return pd.DataFrame({'Groups': pred_y}, index=DataFrame.index)