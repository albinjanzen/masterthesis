import pandas as pd

df = pd.read_csv('data/structured/nordpool_flow.csv', index_col=0)
df2 = df['NO5_NO2_D_FE']
df2.reset_index(drop=True, inplace=True)
mask = df2 == 0
mask = mask[1:]
df2 = df2[:-1]
print(mask)
print(df2)
print(df2[df2 == 0])

