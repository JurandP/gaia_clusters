import argparse
import prepare_database.parts_of_prepare
import pandas as pd

# solution for problem with using boolean values in arparse founded in
# https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def prepare_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bin_size", type=int,
        help="Add size of bins to divide spectrum. Default --bin_size = 3", default=3)
    parser.add_argument("-m", "--only_max", type=str2bool,
        help="Use only information about spectra in maximum of lightcurve. \
         Default --only_max = True", default=True)
    parser.add_argument("-i", "--interpolation", type=str2bool,
        help="Use linear interpolation to lightcurve and make tsfresh \
         statistics on interpolated curve.Default = False", default=False)
    parser.add_argument("-t", "--tsfresh", type=str2bool,
        help="Use tsfresh statistics to prepare database. Default --tsfresh = True",
        default=True)
    parser.add_argument("-l", "--min_mag", type=str,
        help="Minimum magnitude of objects in their maximum. \
         Objects with lower magnitude will be removed in preparation of database. \
         If None, all of objects will be processed. Default --min_mag = None", default=None)
    parser.add_argument("-j", "--n_jobs", type=int, 
    help="Number of processes to prepare database. n_jobs > 1 only on unix operation systems. \
         Default n_jobs=1", default=1)
    parser.add_argument("-d", "--download_database", type=str2bool,
        help="Download raw data. Default --download_database = False",
        default=False)
    parser.add_argument("-e", "--preprocessing", type=str2bool,
        help="Make preprocessing of data. Default --preprocessing = True",
        default=True)
    parser.add_argument("-p", "--postprocessing", type=str2bool,
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
    if args.min_mag == 'None' or  args.min_mag == 'none':
        min_mag = None
    else:
        min_mag = float(args.min_mag)
    download_database = args.download_database
    preprocessing = args.preprocessing
    postprocessing = args.postprocessing

    if bin_size >= 60 or bin_size <= 0:
        raise ValueError("Bin_size value is not in range (1, 60).")
    if not tsfresh and not only_max:
        raise OtherException("It is required to use tsfresh with processing each spectra. \
        To use the version without tsfresh, set option only_max = True.")
    if only_max and interp:
        raise OtherException("When only_max = True, there are no data to interpolate. \
        Set interp = False, or to use 1d interpolation, set only_max = False")
        
    # names of suffixes of files, preproc_suffix_name
    # to preprocessing, suffix_name to postprocessing
    suffix_name = '_' + str(bin_size) + 'bin'
    preproc_suffix_name = suffix_name
    if interpolation:
        suffix_name += '_interp'
    if only_max:
        suffix_name += '_only_max'
    if not min_mag==None:
        suffix_name += '_' + str(min_mag)
    if tsfresh:
        suffix_name += '_' + 'tsfresh'

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
        prepare_database.parts_of_prepare.make_download_database(alerts=alerts)

    if preprocessing:
        prepare_database.parts_of_prepare.make_preprocessing_database(
            alerts=alerts,
            n_jobs=n_jobs,
            size_of_bin=bin_size, suffix = preproc_suffix_name)
    
    if postprocessing:
        prepare_database.parts_of_prepare.make_postprocessing(
            alerts=alerts, int_begin=int_begin, int_end=int_end,
            number_of_post_processed=number_of_post_processed, size_of_bin=bin_size,
            only_max=only_max, min_mag=min_mag, tsfresh=tsfresh, suffix = suffix_name)
        if not only_max:
            prepare_database.parts_of_prepare.save_database(
                number_of_post_processed=number_of_post_processed, suffix = suffix_name)

    
if __name__ == '__main__':
    main()
