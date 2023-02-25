import pandas as pd
import numpy as np
import os
import csv

from itertools import repeat
from prepare_database.functions import Final_res
from prepare_database.interpolation import Produce_vect

def normalize(arr):
    arr = np.array(arr)
    x = arr/arr.sum()
    x = x.round(5)

    return list(x)

# simple feature to make string from list without set delimiter
def list_to_string(s, delimiter):

    string_to_return = ""
    for i in s:
        string_to_return += str(i) + delimiter
    return string_to_return[:-len(delimiter)]

raw_dir = 'Raw_data'
alerts = pd.read_csv('alerts.csv')['#Name']

def postprocessing_data(name, size_of_bin = 3, interp = False,
    only_max = True, tsfresh = True, light_power = None, suffix = ''):

    # read data from raw
    df = pd.read_csv('Data/' + 'Raw_data/' + name + '_lightcurve.csv', header=1)
    
    if light_power == None:
        light_power = 1000.0

    # find maximum of brightness and its time
    try:
        df = df[df['averagemag'] != 'untrusted']
        index_of_max = float(round(df.sort_values(by=['averagemag']).iloc[0,1], 2))
        max_value = float(df.sort_values(by=['averagemag']).iloc[0,2])
    except IndexError:
        with open('Data/' + 'Little_Data' + suffix + '.csv', 'a') as input:
            input.write(name + '\n')
        return -1
                                

    if only_max:
        # remove unnecessary data and change of format
        df = df[pd.to_numeric(df['averagemag'], errors='coerce').notnull()]
        df = df[df['averagemag'] != 'NaN']
        df['averagemag'] = df['averagemag'].apply(float)
        df = df.drop(['#Date','JD(TCB)'], axis=1)
    
        if len(df) > 4 and max_value < light_power:
            if os.path.exists(
                'Data/' + 'Preprocessed_data' + str(size_of_bin) + \
                'bin' + '/' + name + '_processed.csv'
                ) and os.stat(
                'Data/' + 'Preprocessed_data' + str(size_of_bin) + \
                'bin' + '/' + name + '_processed.csv').st_size > 0:
                tsfresh_stat = Final_res(df)
                df = pd.read_csv('Data/' + 'Preprocessed_data' + \
                str(size_of_bin) + 'bin' + '/' + name + '_processed.csv',
                header = None , delim_whitespace=True)
                df.index = df[0]
                if index_of_max in df[0].to_list():
                    if tsfresh:
                        s = [name] + tsfresh_stat + normalize(df.loc[index_of_max].iloc[1:].to_list())
                    else:
                        s = [name] + normalize(df.loc[index_of_max].iloc[1:].to_list())
                    with open('Data/' + 'Final_Database' + suffix + '.csv', 'a') as input:
                        write = csv.writer(input)
                        write.writerow(s)
        else:
            with open('Data/' + 'Little_Data' + suffix + '.csv', 'a') as input:
                input.write(name + '\n')
    if not only_max and max_value < light_power:
        if os.path.exists(
            'Data/' + 'Preprocessed_data' + str(size_of_bin) + 'bin' + '/' + name + '_processed.csv'
            ) and os.stat(
            'Data/' + 'Preprocessed_data' + str(size_of_bin) + 'bin' + '/' + name + '_processed.csv').st_size > 0:
            df = pd.read_csv('Data/' + 'Preprocessed_data' + str(size_of_bin) + 'bin' + '/' + name + '_processed.csv',
            header = None , delim_whitespace=True)
            df = Produce_vect(df, size_of_bin = size_of_bin, interp = interp)
            CollectedData = Final_res(df)
            
            if not np.isnan(CollectedData).any():
                return name + ', ' + list_to_string(CollectedData, ', ') + '\n'
            else:
                with open('Data/' + 'Little_Data' + suffix + '.csv', 'a') as input:
                    input.write(name + '\n')

    print(name + ' postprocessing is done.')

def make_file_with_database(
    alerts_names_base, filename, processes_number = 1, size_of_bin = 3,
    interp = False, only_max = True, tsfresh = True, min_mag=None, suffix = ''):
    Data = []
    if processes_number > 1:
        import multiprocessing as mp

        pool =  mp.Pool(processes=processes_number)
        try:
            Data = pool.starmap(postprocessing_data, zip(alerts_names_base, repeat(size_of_bin),
                repeat(interp), repeat(only_max), repeat(tsfresh),
                repeat(min_mag), repeat(suffix)))
        except mp.TimeoutError:
            print("We lacked patience and got a multiprocessing.TimeoutError")
        pool.close()
    else:
        for i in alerts_names_base:
            Data.append(postprocessing_data(i, size_of_bin = size_of_bin, interp = interp,
                only_max = only_max, light_power=min_mag, suffix = suffix))

    Data = [i for i in Data if not i == None]

    with open(filename, 'w') as input:
        for i in Data:
            input.write(i)

# function collects the data in their average and puts it into containers of length size_of_bin
# example: 1.0 2.0 3.0 4.0 5.0 6.0, size_of_bin = 3 -> 2.0 7.5
def preprocessing_data(filename, size_of_bin = 3, suffix = ''):
    text = ""
    with open('Data/' + raw_dir + '/' + filename + '_spectrum.csv', 'r') as input:
        while True:
            s = input.readline()
            if not s:
                break
            s = list(s.strip().split(', '))
            s = [float(x) for x in s]
            mod_s = [round(s[0],size_of_bin)]
            number_of_bins = int(120/size_of_bin)
            
            for j in range(1,1 + number_of_bins):
                s_mean = np.mean(s[(j-1)*size_of_bin+1 : j*size_of_bin+1 : 1])
                mod_s.append(round(s_mean , 4))
            text = text + list_to_string(mod_s, ' ') + "\n"

    with open('Data/' + 'Preprocessed_data' + suffix + '/' + filename + '_processed.csv', 'w') as input:
        input.write(text)
    print(filename, ' preprocessing is done')

