import argparse
import parts_of_prepare
import pandas as pd

def prepare_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bin_size", type=int,
        help="Add size of bins to divide spectrum. Default --bin_size = 3", default=3)
    parser.add_argument("-m", "--only_max", type=bool,
        help="Use only information about spectra in maximum of lightcurve. \
         Default --only_max = True", default=True)
    parser.add_argument("-i", "--interpolation", type=bool,
        help="Use linear interpolation to lightcurve and make tsfresh \
         statistics on interpolated curve.Default = False", default=False)
    parser.add_argument("-t", "--tsfresh", type=bool,
        help="Use tsfresh statistics to prepare database. Default --tsfresh = True",
        default=True)
    parser.add_argument("-l", "--min_mag", type=float,
        help="Minimum magnitude of objects in their maximum. \
         Objects with lower magnitude will be removed in preparation of database. \
         If None, all of objects will be processed. Default --min_mag = None", default=None)
    parser.add_argument("-j", "--n_jobs", type=int, 
    help="Number of processes to prepare database. n_jobs > 1 only on unix operation systems. \
         Default n_jobs=1", default=1)
    parser.add_argument("-d", "--download_database", type=bool,
        help="Download raw data. Default --download_database = False",
        default=False)
    parser.add_argument("-e", "--preprocessing", type=bool,
        help="Make preprocessing of data. Default --preprocessing = True",
        default=True)
    parser.add_argument("-p", "--postprocessing", type=bool,
        help="Make postprocessing of data. Default --postprocessing = True",
        default=True)
    return parser.parse_args()

def main():
    # read options from argpare
    args = prepare_argparse()

    # add options and return exception if needed
    bin_size = args.bin_size
    interpolation = args.interpolation
    only_max = args.only_max
    tsfresh = args.tsfresh
    n_jobs = args.n_jobs
    min_mag = args.min_mag
    download_database = args.download_database
    preprocessing = args.preprocessing
    postprocessing = args.postprocessing

    if bin_size >= 60 or bin_size <= 0:
        raise ValueError("Bin_size value is not in range (1, 60).")
    
    #CONFIG
    #names of files, initial variables for main script
    filename = "alerts.csv"
    #determining which data from alerts to process
    int_begin = 0
    int_end = 20670
    #number of .csv files with post processed data
    number_of_post_processed = 5


    #pandas dataframe with basic data about alerts
    alerts = pd.read_csv(filename).loc[int_begin : int_end]

    if download_database:
        parts_of_prepare.make_download_database()

    if preprocessing:
        parts_of_prepare.make_preprocessing_database(
            alerts=alerts,
            n_jobs=n_jobs,
            interpolation=interpolation,
            size_of_bin=bin_size)
    
    if postprocessing:
        parts_of_prepare.make_postprocessing(
            alerts=alerts, int_begin=int_begin, int_end=int_end,
            number_of_post_processed=number_of_post_processed, size_of_bin=bin_size,
            only_max=only_max, min_mag=min_mag, tsfresh=tsfresh)
        parts_of_prepare.save_database(bin_size=bin_size, interpolation=interpolation, 
        only_max=only_max, min_mag=min_mag, tsfresh=tsfresh)

    
if __name__ == '__main__':
    main()