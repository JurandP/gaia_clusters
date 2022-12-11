import numpy as np
import pandas as pd

from sklearn import metrics
from clustering.additional_tools import read_json

config = read_json('configs/config.json')
df = pd.read_csv(config['result_name'] + '_dataframe.csv')

print(df)

for i in df.index:
    print(i)