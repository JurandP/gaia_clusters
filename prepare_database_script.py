import pandas as pd
import concurrent.futures
#import multiprocessing as mp

from prepare_database.download_database import make_spectrum_csv
from prepare_database.download_database import check_folder
from prepare_database.processing_database import preprocessing_data
from prepare_database.processing_database import make_file_with_database, preprocessing_data

#names of files, initial variables for main script
filename = "alerts.csv"
#determining which data from alerts to process
int_begin = 0
int_end = 20670
#number of processors used in calculations
processes_number = 2
#number of .csv files with post processed data
number_of_post_processed = 5
size_of_bin = 3
interp = 0

#pandas dataframe with basic data about alerts
alerts = pd.read_csv(filename).loc[int_begin : int_end]

# #RAW DATA
# check_folder('Raw_data')
# #creates separate data files about spectra and lightcurves in Raw_data directory 
# paths = ['http://gsaweb.ast.cam.ac.uk/alerts/alert/' + i + '/' for i in alerts['#Name']]
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     future_to_url = {executor.submit(make_spectrum_csv, i): i for i in alerts['#Name']}

# print('SCRIPT DID 1/4 OF THE WORK -- Downloading raw data is done!')

# PREPROCESSING DATA
# check_folder('Preprocessed_data')

# pool =  mp.Pool(processes=processes_number)
# try:
#         pool.map(preprocessing_data, alerts['#Name'])
# except mp.TimeoutError:
#         print("We lacked patience and got a multiprocessing.TimeoutError")
# pool.close()

# for i in alerts['#Name']:
#    preprocessing_data(i, size_of_bin = size_of_bin)

# print('SCRIPT DID 2/4 OF THE WORK -- Preprocessing is done!')

#POSTPROCESSING DATA
check_folder('Postprocessed_Database')

#check if file with names of broken or too small data is empty 
f = open('Little_Data.csv', 'w')
f.close()
f = open('Final_Database.csv', 'w')
f.close()


#make post_processing file
number_of_objects_in_file = int((int_end - int_begin + 1) / number_of_post_processed)

for i in range(0,number_of_post_processed):
    make_file_with_database(alerts['#Name'].loc[
        i*number_of_objects_in_file : 
        (i+1)*number_of_objects_in_file-1], 'Postprocessed_Database/'+str(i) +'.csv', size_of_bin = size_of_bin, interp = interp) 

print('SCRIPT DID 3/4 OF THE WORK -- Postprocessing is done!')

#FINAL DATAFRAME        
#final_file = ""
#Adding data from Postprocessed_Database/ to single dataframe
#for i in range(0,number_of_post_processed):
#    with open('Postprocessed_Database/'+str(i)+'.csv') as input:
#        final_file += input.read() + '\n'
#    with open('Final_Database.csv', 'w') as input:
#	    input.write(final_file)
        
print('SCRIPT DID THE WORK -- make Final_Database.csv is done!')
