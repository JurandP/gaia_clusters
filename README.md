# GaiaClusters
This project was created as a bachelor's degree in astronomy at the University of Warsaw. Its purpose is to collect data on the alerts of the space mission Gaia and to attempt clustering using various methods. The exact operation of the individual components of the project, as well as the documentation of the results, are included in the text of the thesis, available via Overleaf:

(link after graduation)

## Prepare database
### Description
Package created to prepare input database for clustering algorithms. There are three phases of preparation: download raw database, preprocessing to merge data from lightcurve with spectra and finally to make postprocessing. Postprocessing marks points of binded spectrum from each observations in one row of final database. It could be done with only spectra's data of maximum brightness with ``only_max`` parameter. When ``only_max`` is made there are possibility to add to database tsfresh parameters of lightcurve by setting ``tsfresh = True``. In postprocessing, when ``only_max = False`` there is possibility to interpolate lightcurve data on timescale 2014-2022.
### Run
From parent directory of project could be run with
```
python3.8 -m prepare_database \
    --bin_size 3 \
    --only_max False \
    --interpolation False \
    --tsfresh False \
    --min_mag 17.0 \
    --n_jobs 21 \
    --download_database False \
    --preprocessing True \
    --postprocessing True
```
 
where:
  * ``bin_size`` is size of frequency's bin to save spectra from particular event;
  * ``only_max`` if you want to produce database where spectra datas are only from maximum brightness;
  * ``interpolation`` make 1d interpolation on lightcurve to produce more points to tsfresh analysis;
  * ``tsfresh`` switch to set statistical parameters from tsfresh module - optional;
  * ``min_mag`` minimal value of objects brightness (in mag) in it's maximum. Objects with lower maximum brightness will be ommited from database creation;
  * ``n_jobs`` number of workers to produce database. n_jobs > 1 only on unix base systems;
  * ``download_database`` produce a directory ``Raw_data/`` with raw data;
  * ``preprocessing`` produce a directory with binded points in spectras;
  * ``postprocessing`` merge points in one final database. Could be done with interpolation and tsfresh statistical parameters

There is also bash script to run with some parameters:

```
bash scripts/run_prepare_database.sh
```
## Clustering
### Basic description
The second package is for clustering. Clustering is made by five methods from ``sklearn.clusters``:
* BIRCH,
* KMeans,
* Bisecting KMeans,
* Mini Batch KMeans,
* Agglomerative Clustering with ward.

Before clustering, datas are standarized by removing outliers (with ``sklearn.neighbors.LocalOutlierFactor``), normalize data in columns and also principal component analysis. To do PCA, there is necessary ``vec_proc`` parameter in range (0,1) and to remove outliers, given class needs ``n_neighbors``. After run, the package print in the screen information about shape of database before and after non-clustering operations described above.

### Metrics
To describe quality of clustering by given method, I invented simple metrics, introduced by:

> sum over predicted labels from (biggest group from true labels) / sum of all labeled objects. 

In ``alerts.csv`` there is label `` Class`` which was base to construct metrics. Value of metrics is in range (0,1), and the bigger value of metrics is better. Value of metrics is printed on screen, below the name of each method. The second tag of good clustering is confusion matrix. Matrices are saved in ``/Data/ConfusionMatricesPNG_suffix_name`` and there is special true label 'unknown', added to track results of clustering on unidentified objects.

### Run
From parent directory of project could be run with
```
python3.8 -m clustering \
    --suffix_name 3bin_only_max_tsfresh \
    --n_jobs 2 \
    --n_clusters 8 \
    --n_neighbors 10 \
    --vec_perc 0.85

```
 
where:
  * ``suffix_name`` is index of dataframe to clustering;
  * ``n_jobs`` is number of processes to execute the script;
  * ``n_clusters`` is number of clusters to make;
  * ``n_neighbors`` is parameter of method to remove outliers;
  * ``vec_perc`` is parameter in range (0,1) describing the number of vectors not removed by pca.




## Optimization
Simple module to optimize parameters of clustering ``n_clusters``, ``n_neighbors`` and ``vec_proc``. There is a necessary argument ``--suffix_name`` to get database in format Final_Database_suffix_name.csv. Optimalized value is gaia_clusters metrics via grid search.


## Dependencies
Python modules:
* sklearn < 1.4.0
* tsfresh
* numpy
* pandas
* scipy
* argparse

## Installation
Project is installable by bash command with git:

```
cd
git clone git@github.com:JurandP/gaia_clusters.git \
cd ~/gaia_clusters
pip install -e .

```
