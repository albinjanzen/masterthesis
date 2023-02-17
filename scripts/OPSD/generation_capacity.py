
import pandas as pd
import os

filename = 'national_generation_capacity.csv'
raw_file = 'national_generation_capacity_stacked_filtered.csv'
path_to_raw = '../../data/Raw/OPSD/'
path_to_structured = '../../data/Structured/'

if os.path.exists(path_to_structured + filename):
    os.remove(path_to_structured + filename)


df = pd.read_csv(path_to_raw + raw_file, sep=',',
                 parse_dates=['year'])
df = df[df['country'] == 'SE']
df = df[df['capacity'] != 0]
df.sort_values(by=['year'], inplace=True)
df.drop(columns=['source', 'source_type', 'capacity_definition',
                 'comment', 'country', 'type', 'technology_level', 'energy_source_level_0', 'energy_source_level_1', 'energy_source_level_2', 'energy_source_level_3'], inplace=True)
df.rename(columns={'year': 'Date'}, inplace=True)
df['capacity'] = df.groupby(['Date', 'technology'])[
    'capacity'].transform('mean')
df.drop_duplicates(subset=['Date', 'technology'], inplace=True)
df = df.pivot(index='Date', values='capacity', columns=[
    'technology'])
print(df)
df.to_csv(path_to_structured + filename, index=True)
