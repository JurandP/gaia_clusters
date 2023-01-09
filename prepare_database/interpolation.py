import pandas as pd
import numpy as np

from scipy.interpolate import interp1d

dates = np.arange(2456666.25, 2459727.50, 1000.0)

def interpolation(time, vect):
	try:
		line = interp1d(time, vect, kind = 'linear')
	except ValueError:
		return [0]*len(dates)
	buff = []
	for j in dates:
		if time[0] < j and j < time[-1]:
			buff.append(float(line(j)))
		else:
			buff.append(0.0)
	return buff

def Produce_vect(df, size_of_bin = 3, interp = 1):
        index = [i for i in range(1, len(df))] + [0]
        df = df.reindex(index)
        time = df[0].values.tolist()
        if interp == 1:
	    processes = [interpolation(time,df[i].values.tolist()) for i in range(1, 1+ int(120/size_of_bin))]
        else:
	    processes = [df[i].values.tolist() for i in range(1, 1+ int(120/size_of_bin))]
        results = [i for i in processes]
        return pd.DataFrame(results).T
		
