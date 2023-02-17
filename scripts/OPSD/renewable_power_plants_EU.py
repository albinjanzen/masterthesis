import pandas as pd
import os

filename = 'renewable_power_plants.csv'
raw_file = 'renewable_power_plants_EU_filtered.csv'
path_to_raw = '../../data/Raw/OPSD/'
path_to_structured = '../../data/Structured/'

if os.path.exists(path_to_structured + filename):
    os.remove(path_to_structured + filename)

df = pd.read_csv(path_to_raw + raw_file, sep=',', parse_dates=['as_of_year'])
df.rename(columns={'commissioning_date': 'Date'}, inplace=True)
df.drop(columns=['as_of_year', 'lat', 'lon',
                 'geographical_resolution', 'technology', 'nuts_1_region', 'nuts_2_region', 'nuts_3_region', 'municipality', 'data_source', 'energy_source_level_1', 'energy_source_level_2', 'energy_source_level_3'], inplace=True)
df = df.groupby(['Date', 'country']).agg({'electrical_capacity': 'sum'})
df.reset_index(inplace=True)
df.columns = ['Date', 'country', 'electrical_capacity']
print(df.columns)
df = df.pivot(columns='country', values='electrical_capacity', index='Date')
print(df)
print(df.shape)
df['Date'] = df.index
df.reset_index(drop=True, inplace=True)
df['Date'] = pd.to_datetime(df['Date'])

df['Date'] = df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
df.to_csv(path_to_structured + filename, index=False)
