import clustering.additional_tools as cladd
import pandas as pd

df_1 = pd.DataFrame({'Groups': [4, 4, 4, 8, 5, 5, 7]}, index=['a', 'b', 'c', 'd', 'e', 'f', 'g'])
df_2 = pd.DataFrame({'Type': [1, 1, 1, 1, 2, 2, 3]}, index=['a', 'b', 'c', 'd', 'e', 'f', 'g'])
df = pd.DataFrame({'Groups': [4, 4, 4, 8, 5, 5, 7, 9, 11, 1],
 'Type': [1, 1, 1, 1, 2, 2, 3, 8, 9, 123], 
 'Groups3': [4, 4, 4, 8, 5, 5, 7, 9, 11, 1],
 'Groups4': [2, 5, 6, 12, 124, 8, 11, 9, 11, 7]},
  index=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])

print(df)
df = cladd.standarization(df)
print(cladd.principal_component_analysis(df))
print(cladd.make_metrics(df))