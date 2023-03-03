# GaiaClusters
This project was created as a bachelor's degree in astronomy at the University of Warsaw. Its purpose is to collect data on the alerts of the space mission Gaia and to attempt clustering using various methods. The exact operation of the individual components of the project, as well as the documentation of the results, are included in the text of the thesis, available via Overleaf:

(link after graduation)

## Prepare database
### Description
Package created to prepare input database for clustering algorithms. There are three phases of preparation: download raw database, preprocessing to merge data from lightcurve with spectra and finally to make postprocessing. Postprocessing marks points of binded spectrum from each observations in one row of final database. It could be done with only spectra's data of maximum brightness with ``only_max`` parameter. When ``only_max`` is made there are possibility to add to database tsfresh parameters of lightcurve by setting ``tsfresh = True``. In postprocessing, when ``only_max = False`` there is possibility to interpolate lightcurve data on timescale 2014-2022  
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

## Dependencies
Python modules:
* sklearn < 1.4.0
* tsfresh
* numpy
* pandas
* scipy

All of the scripts can be executed if there is a file processed by script. All of the modules and scripts works with Python3.8.pip
'''
python3.8 download_database_script.py

'''
ts_fresh, numpy, pandas, multiprocessing, json, scipy required, download files from gsaweb.ast.cam.ac.uk.


