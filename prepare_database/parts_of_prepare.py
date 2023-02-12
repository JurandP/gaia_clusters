import concurrent.futures

from prepare_database.download_database import make_spectrum_csv
from prepare_database.download_database import check_folder
from prepare_database.processing_database import preprocessing_data
from prepare_database.processing_database import make_file_with_database, preprocessing_data

def make_download_database(alerts):
    check_folder('Raw_data')
    #creates separate data files about spectra and lightcurves in Raw_data directory 
    paths = ['http://gsaweb.ast.cam.ac.uk/alerts/alert/' + i + '/' for i in alerts['#Name']]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(make_spectrum_csv, i): i for i in alerts['#Name']}

    print('SCRIPT DID 1/4 OF THE WORK -- Downloading raw data is done!')

def make_preprocessing_database(alerts, n_jobs=1, size_of_bin=3):
    check_folder('Preprocessed_data')

    if n_jobs > 1:
        import multiprocessing as mp

        pool =  mp.Pool(processes=n_jobs)
        try:
            pool.map(preprocessing_data, alerts['#Name'])
        except mp.TimeoutError:
            print("We lacked patience and got a multiprocessing.TimeoutError")
        pool.close()

    if n_jobs == 1:
        for i in alerts['#Name']:
            preprocessing_data(i, size_of_bin = size_of_bin)
    
    print('SCRIPT DID 2/4 OF THE WORK -- Preprocessing is done!')

def make_postprocessing(alerts, int_end=20670, int_begin = 0,
    number_of_post_processed = 5, size_of_bin = 3, interpolation = False, tsfresh = True):
    check_folder('Postprocessed_Database')

    #check if file with names of broken or too small data is empty 
    with open('Little_Data.csv', 'w'):
        pass

    #make post_processing file
    number_of_objects_in_file = int((int_end - int_begin + 1) / number_of_post_processed)

    # divide data on parts saved in .csv
    # if some data is invalid, you can remake postprocessing from set place
    for i in range(0,number_of_post_processed):
        make_file_with_database(alerts['#Name'].loc[
            i*number_of_objects_in_file : 
            (i+1)*number_of_objects_in_file-1], 'Postprocessed_Database/'+str(i) +'.csv',
            size_of_bin = size_of_bin, interp = interpolation, tsfresh=tsfresh) 

    print('SCRIPT DID 3/4 OF THE WORK -- Postprocessing is done!')

def save_database(number_of_post_processed = 5, bin_size = 3,
    interpolation = False, only_max = True, min_mag = None, tsfresh = True):
    final_file = ""
    #Adding data from Postprocessed_Database/ to single dataframe
    for i in range(0,number_of_post_processed):
        with open('Postprocessed_Database/'+str(i)+'.csv') as input:
            final_file += input.read() + '\n'
        database_name = 'final_database_'+str(bin_size) + 'bin_'
        if interpolation:
            database_name += 'interp_'
        if only_max:
            database_name += 'only_max_'
        if not min_mag==None:
            database_name += str(min_mag) + '_'
        if tsfresh:
            database_name += 'tsfresh'
        with open(database_name + '.csv', 'w') as input:
	        input.write(final_file)

    print('SCRIPT DID THE WORK -- make Final_Database.csv is done!')