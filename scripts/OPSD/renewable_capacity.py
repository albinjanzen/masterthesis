import pandas as pd
import os
filename = 'renewable_capacity.csv'
raw_file = 'renewable_capacity_timeseries_filtered.csv'
path_to_raw = '../../data/Raw/OPSD/'
path_to_structured = '../../data/Structured/'

if os.path.exists(path_to_structured + filename):
    os.remove(path_to_structured + filename)
df = pd.read_csv(path_to_raw + raw_file, sep=',', parse_dates=['day'])
print(df)
df.rename(columns={'day': 'Date'}, inplace=True)

df['Date'] = df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
df.to_csv(path_to_structured + filename, index=False)
