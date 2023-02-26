import requests
import re
import os
import urllib
from threading import Lock

raw_dir_name = 'Raw_data'

#check if dir_name folder to save data exists. If not it is created
def check_folder(dir_name):
	if not os.path.exists(dir_name):
		os.mkdir(dir_name)

#Additional function to count how many alerts is downloaded
def count_alerts():
	if 'GLOBAL_INDEX' not in globals():
		global GLOBAL_INDEX
		GLOBAL_INDEX = 1
	else:
		with Lock(): 
			GLOBAL_INDEX += 1
			if GLOBAL_INDEX % 100 == 0:
				print(GLOBAL_INDEX)


#main function in this module, create files #alertname_lightcurve.csv and #alertname_spectrum.csv for given name
def make_spectrum_csv(name):
	#creating url link to download
	path_spectrum = 'http://gsaweb.ast.cam.ac.uk/alerts/alert/' + name + '/'
	path_lightcurve = path_spectrum + 'lightcurve.csv'
	#download data for given alert from gsaweb.ast.cam.ac.uk
	string = str(requests.get(path_spectrum).content)
	urllib.request.urlretrieve(path_lightcurve,'Data/' + raw_dir_name +'/' + name + '_lightcurve.csv' )
	print(name)
	#using re to find in html spectrum data
	indexes = re.findall(r'<td>(.*?)<', string)
	#blue photometer
	bp = re.findall(r'"bp": \[(.*?)]', string)
	#red photometer
	rp = re.findall(r'"rp": \[(.*?)]', string)
	
	#write indexes, rp and bp strings to file _spectrum.csv
	with open('Data/' + raw_dir_name +'/' + name + '_spectrum.csv', 'w') as input:
		for i in range(len(rp)):
			input.write(indexes[2*i-1] + ', ')
			input.write(bp[i] + ', ')
			input.write(rp[i] + '\n')
	count_alerts()

#Check if some data from alertslist doesn't exist or is empty
def valid_data_test(df_names):
	with open('Data/' + raw_dir_name + '/MISSING_DATA_RAPORT.csv', 'w') as input:
		input.write('Missing spectrum for the following data: \n') #part for spectra
		for i in df_names:
			if os.path.exists('Data/' + raw_dir_name + '/' + i + '_spectrum.csv') == False:
				input.write(i)
			else:
				if os.path.getsize('Data/' + raw_dir_name + '/' + i + '_spectrum.csv') == 0.0:
					input.write(i, ' empty file')
		input.write('Missing lightcurve for the following data: \n') #part for lightcurve
		for i in df_names:
			if os.path.exists('Data/' + raw_dir_name + '/' + i + '_lightcurve.csv') == False:
				input.write(i)
			else:
				if os.path.getsize('Data/' + raw_dir_name + '/' + i + '_lightcurve.csv') == 0.0:
					input.write(i, ' empty file')
			
