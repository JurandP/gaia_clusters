import pandas as pd
import numpy as np

from scipy.stats import entropy
import tsfresh.feature_extraction.feature_calculators as ts

#test_df = pd.read_csv('Proceed_data'+'/' + 'Gaia22cxr' + '_proceed.csv',header = None ,delimiter = ' ')

def median_deviation(x):
	a = x.median()
	x = x-a
	return x.apply(abs).median()

def is_num(x):
	if type(x) == float: return 1
	else: return 0

def consecutive_obs(df, mean):
	mean  = float(mean)
	df = pd.DataFrame(df)
	df.columns = ['x']
	df['y'] = 0.0

	df.loc[(df['x'].shift(1) > mean) & (df['x'].shift(2) > mean) & (df['x'] > mean), 'y'] = 1
	df.loc[(df['x'].shift(1) < mean) | (df['x'].shift(2) < mean) | (df['x'] < mean), 'y'] = 0
	a = float((df['y'] != df['y'].shift()).cumsum().tail(1))


	if float(df['y'].head(1)) == 0.0 and float(df['y'].tail(1)) == 0.0 :
		a = (a-1.0)/2.0
	elif float(df['y'].head(1)) == 1.0 and float(df['y'].tail(1)) == 1.0 :
		a = (a+1.0)/2.0
	else:
		a = a/2.0

	return a

def entropy_funct(x):
	return entropy(x.value_counts())
	
def delta_funct(x, i):
	return 1.02597835209 * (x.loc[i] - x.mean())/x.std(ddof=1)
	
def summed_StetsonJ(x):
	S = 0.0
	for i in range(0, len(x) -1):
		a = delta_funct(x, i)*delta_funct(x, i+1)
		S += np.sign(a)*np.sqrt(abs(a))
	return S
	
def summed_StetsonK(x):
	S_1 = 0.0
	S_2 = 0.0
	for i in range(0, len(x)):
		S_1 += abs(delta_funct(x,i))
		S_2 += delta_funct(x,i)*delta_funct(x,i)
	return 0.22360679775 * S_1 / np.sqrt(S_2)
	
	
	
############################################################
def Above1(df):
	return (df[(df > (df.mean()+df.std(ddof=0))) | (df < (df.mean()-df.std(ddof=0)))]).count()
	

def Above3(df):
	return (df[(df > (df.mean()+3*df.std(ddof=0))) | (df < (df.mean()-3*df.std(ddof=0)))]).count()

def Above5(df):
	return (df[(df > (df.mean()+5*df.std(ddof=0))) | (df < (df.mean()-5*df.std(ddof=0)))]).count()	
	
def AbsoluteEnergy(df):
	return df.apply(ts.abs_energy)
	
def AbsoluteSumofChanges(df):
	return df.apply(ts.absolute_sum_of_changes)
	
def Amplitude(df):
	return df.quantile(q=0.02, numeric_only=True) - df.quantile(q=0.98, numeric_only=True)
	
#Jaki lag??
def Autocorrelation(df):
	return df.apply(lambda x: ts.autocorrelation(x, 1))

def Below1(df):
	return (df[(df < (df.mean()+df.std(ddof=0))) & (df > (df.mean()-df.std(ddof=0)))]).count()
	
def Below3(df):
	return (df[(df < (df.mean()+3*df.std(ddof=0))) & (df > (df.mean()-3*df.std(ddof=0)))]).count()
	
def Below5(df):

	return (df[(df < (df.mean()+5*df.std(ddof=0))) & (df > (df.mean()-5*df.std(ddof=0)))]).count()
	
#Jaki lag?	
def C3(df):
	return df.apply(lambda x: ts.c3(x, 0))

#Duplicates functions check how many times certain object is repeated
def CheckDuplicates(df):
	return df.apply(ts.has_duplicate)
	#return df.groupby('time').count()[1] - 1
	
def CheckMaxDuplicates(df):
	return df.apply(ts.has_duplicate_max)
	#return df[df == df.max()].count()-1
	
def CheckMinDuplicates(df):
	return df.apply(ts.has_duplicate_min)
	#return df[df == df.min()].count()-1
	
def CheckMaxLastLoc(df):
	return df.apply(ts.last_location_of_maximum)

def CheckMinLastLoc(df):
	return df.apply(ts.last_location_of_minimum)
	
#normalize chyba false??
def Complexity(df):
	return df.apply(lambda x: ts.cid_ce(x, False))
	
def Con(df):
	return df.apply(lambda x: consecutive_obs(x, x.mean()+3.0*x.std(ddof=0)))

def Con2(df):
	return df.apply(lambda x: consecutive_obs(x, x.mean()+2.0*x.std(ddof=0)))

def CountAbove(df):
	return df[df>df.mean()].count()

def CountBelow(df):
	return df[df<df.mean()].count()

def FirstLocMax(df):
	return df.apply(ts.first_location_of_maximum)
	
def FirstLocMin(df):
	return df.apply(ts.first_location_of_minimum)
		
def Integrate(df):
	return df.sum()/2.0
	
def Kurtosis(df):
	return df.apply(ts.kurtosis)

def LongestStrikeAbove(df):
	return df.apply(ts.longest_strike_above_mean)

def LongestStrikeBelow(df):
	return df.apply(ts.longest_strike_below_mean)
	
def MeanAbsoluteChange(df):
	return df.apply(ts.mean_abs_change)
	
def MeanChange(df):
	return df.apply(ts.mean_change)
	
def MeanSecondDerivative(df):
	return df.apply(ts.mean_second_derivative_central)

def MedianAbsoluteDeviation(df):
	return df.apply(lambda x: median_deviation(x))


def MedianBufferRange(df):
	x = df.max() - df.min()
	df = df[(df < abs(df.mean() + (df.max() - df.min())/10.0) ) & (df > abs(df.mean() - (df.max() - df.min())/10.0))].count()  
	return df/len(df)
	
def MedianBufferRange2(df):
	x = df.max() - df.min()
	df = df[(df < abs(df.mean() + (df.max() - df.min())/5.0) ) & (df > abs(df.mean() - (df.max() - df.min())/5.0))].count()  
	return df/len(df)
	


def PeakDetection(df):
	return df.apply(lambda x: ts.number_cwt_peaks(x, len(x)))
	

def RatioofRecurringPoints(df):
	return df.apply(ts.percentage_of_reoccurring_values_to_all_values)
	


def RootMeanSquared(df):
	return df.apply(ts.root_mean_square)


def SampleEntropy(df):
	return df.apply(ts.sample_entropy)
	
def ShannonEntropy(df):
	return df.apply(entropy_funct)
	
def Skewness(df):
	return df.apply(ts.skewness)
	
def STD(df):
	return df.std(ddof=0)
		
def STDOverMean(df):
	return df.std(ddof=0)/(df.mean())

def StetsonJ(df):
	return df.apply(summed_StetsonJ)

def StetsonK(df):
	return df.apply(summed_StetsonK)

def StetsonL(df):
	df1 = df.apply(summed_StetsonJ)
	df2 = df.apply(summed_StetsonK)
	return df1*df2 / 0.798

def SumValues(df):
	return df.sum()
	
#lag
def TimeReversalAssymetry(df):
	return df.apply(lambda x: ts.time_reversal_asymmetry_statistic(x, 0))

def vonNeumannRatio(df):
	dff = df.shift(1)
	return ((dff-df)*(dff-df)/len(dff)).sum()/(df.var())
####################################################################	
	
	
def Final_res(df):
	df_res = list(pd.concat([Above1(df), Above3(df), Above5(df), AbsoluteEnergy(df),
	AbsoluteSumofChanges(df), Amplitude(df), Autocorrelation(df), Below1(df), Below3(df),
	Below5(df), C3(df), CheckDuplicates(df), CheckMaxDuplicates(df),  CheckMinDuplicates(df),
	CheckMaxLastLoc(df), CheckMinLastLoc(df), Complexity(df), Con(df),
	Con2(df), CountAbove(df), CountBelow(df), FirstLocMax(df), FirstLocMin(df), Integrate(df),
	Kurtosis(df), LongestStrikeAbove(df), LongestStrikeBelow(df), MeanAbsoluteChange(df),
	#RatioofRecurringPoints(df), RootMeanSquared(df), SampleEntropy(df), ShannonEntropy(df),
	Skewness(df), STD(df), STDOverMean(df),# StetsonJ(df), StetsonK(df), StetsonL(df),
	SumValues(df), TimeReversalAssymetry(df), vonNeumannRatio(df)
	]).round(3))
	return df_res
