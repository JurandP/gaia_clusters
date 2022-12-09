import pandas as pd
import numpy as np
import os
import multiprocessing as mp

from prepare_database.functions import Final_res
from prepare_database.interpolation import Produce_vect

#simple feature to make string from list without set delimiter
def list_to_string(s, delimiter):

    string_to_return = ""
    for i in s:
        string_to_return += str(i) + delimiter
    return string_to_return[:-len(delimiter)]

raw_dir = 'Raw_data'
alerts = pd.read_csv('alerts.csv')['#Name']

#function to open Proceed_data and produce final dataframe
def postprocessing_data(name, size_of_bin = 3, interp = 1):
        if os.path.exists(
                'Preprocessed_data/' + name + '_processed.csv'
                ) and os.stat(
                'Preprocessed_data/' + name + '_processed.csv').st_size > 0:
                        df = pd.read_csv('Preprocessed_data/' + name + '_processed.csv',
                        header = None , delim_whitespace=True)
                        df = Produce_vect(df, size_of_bin = size_of_bin, interp = interp)
                        CollectedData = Final_res(df)
                        if not np.isnan(CollectedData).any():
                                return name + ', ' + list_to_string(CollectedData, ', ')+'\n'
                        else:
                                with open('Little_Data.csv', 'a') as input:
                                        input.write(name + '\n')

def make_file_with_database(AlertsNamesBase, FileName, processes_number = 1, size_of_bin = 3, interp = 1):
        Data = []
        # pool =  mp.Pool(processes=processes_number)
        # try:
        #         Data = pool.map(prepare_data, AlertsNamesBase)
        # except mp.TimeoutError:
        #         print("We lacked patience and got a multiprocessing.TimeoutError")
        # pool.close()
        for i in AlertsNamesBase:
                print(i)
                Data.append(postprocessing_data(i, size_of_bin = size_of_bin, interp = interp))

        Data = [i for i in Data if not i == None]
        File = open(FileName, 'w')
        for i in Data:
                File.write(i)
        File.close()

#function collects the data in their average and puts it into containers of length size_of_bin
# example: 1.0 2.0 3.0 4.0 5.0 6.0, size_of_bin = 3 -> 2.0 7.5
def preprocessing_data(filename, size_of_bin = 3):
        text = ""
        with open(raw_dir + '/' + filename + '_spectrum.csv', 'r') as input:
                while True:
                        s = input.readline()
                        if not s:
                                break
                        s = list(s.strip().split(', '))
                        s = [float(x) for x in s]
                        mod_s = [round(s[0],size_of_bin)]
                        number_of_bins = int(120/size_of_bin)
                        
                        for j in range(1,1+ number_of_bins):
                                s_mean = np.mean(s[(j-1)*size_of_bin+1 : j*size_of_bin+1 : 1])
                                mod_s.append( round(s_mean , 4))
                        text = text + list_to_string(mod_s, ' ') + "\n"

        with open('Preprocessed_data' + '/' + filename + '_processed.csv', 'w') as input:
                input.write(text)
        print(filename, ' preprocessing is done')
