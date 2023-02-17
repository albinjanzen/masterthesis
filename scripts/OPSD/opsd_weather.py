import pandas as pd
import os

filename = 'opsd_weather.csv'
raw_file = 'weather_data_filtered (1).csv'
path_to_raw = '../../data/Raw/OPSD/'
path_to_structured = '../../data/Structured/'

if os.path.exists(path_to_structured + filename):
    os.remove(path_to_structured + filename)

df = pd.read_csv(path_to_raw + raw_file, sep=',',
                 parse_dates=['utc_timestamp'])
df.rename(columns={'utc_timestamp': 'Date'}, inplace=True)
df['Date'] = df['Date'].dt.tz_convert('Europe/Stockholm').dt.tz_localize(None)
df.to_csv(path_to_structured + filename, index=False)
