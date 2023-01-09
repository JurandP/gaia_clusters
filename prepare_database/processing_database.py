import pandas as pd
import numpy as np
import os
import multiprocessing as mp
import csv

from prepare_database.functions import Final_res
from prepare_database.interpolation import Produce_vect

def normalize(arr):
    arr = np.array(arr)
    x = arr/arr.sum()
    x = x.round(5)

    return list(x)

#simple feature to make string from list without set delimiter
def list_to_string(s, delimiter):

    string_to_return = ""
    for i in s:
        string_to_return += str(i) + delimiter
    return string_to_return[:-len(delimiter)]

raw_dir = 'Raw_data'
alerts = pd.read_csv('alerts.csv')['#Name']

#function to open Proceed_data and produce final dataframe
def postprocessing_data(name, size_of_bin = 3, interp = 1, only_max = 1):
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']

        if only_max == 1:
                df = pd.read_csv('Raw_data/' + name + '_lightcurve.csv', header=1)
                index_of_max = float(round(df.sort_values(by=['averagemag']).iloc[0,1], 2))
                df = df[pd.to_numeric(df['averagemag'], errors='coerce').notnull()]
                df = df[df['averagemag'] != 'NaN']
                df['averagemag'] = df['averagemag'].apply(float)
                df = df.drop(['#Date','JD(TCB)'], axis=1)
                
                if len(df) > 4:
                    x = Final_res(df)
                    if os.path.exists(
                    'Preprocessed_data/' + name + '_processed.csv'
                    ) and os.stat(
                    'Preprocessed_data/' + name + '_processed.csv').st_size > 0:
                        df = pd.read_csv('Preprocessed_data/' + name + '_processed.csv',
                        header = None , delim_whitespace=True)
                        df.index = df[0]
                        if index_of_max in df[0].to_list():
                            s = [name] + x + normalize(df.loc[index_of_max].iloc[1:].to_list())
                            with open('Final_Database.csv', 'a') as input:
                                write = csv.writer(input)
                                write.writerow(s)
                else:
                    with open('Little_Data.csv', 'a') as input:
                        input.write(name + '\n')
                        

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

def make_file_with_database(
        AlertsNamesBase, FileName, processes_number = 1, size_of_bin = 3, interp = 1, only_max = 1):
        Data = []
        # pool =  mp.Pool(processes=processes_number)
        # try:
        #         Data = pool.map(prepare_data, AlertsNamesBase)
        # except mp.TimeoutError:
        #         print("We lacked patience and got a multiprocessing.TimeoutError")
        # pool.close()
        for i in AlertsNamesBase:
                print(i)
                Data.append(postprocessing_data(i, size_of_bin = size_of_bin, interp = interp, only_max = only_max))

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

