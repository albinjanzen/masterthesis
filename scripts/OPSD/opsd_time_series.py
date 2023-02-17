import pandas as pd
import os

filename = 'opsd_time_series.csv'
raw_file = 'time_series_60min_singleindex_filtered.csv'
path_to_raw = '../../data/Raw/OPSD/'
path_to_structured = '../../data/Structured/'

if os.path.exists(path_to_structured + filename):
    os.remove(path_to_structured + filename)

df = pd.read_csv(path_to_raw + raw_file, sep=',',
                 parse_dates=['utc_timestamp'])
df.rename(columns={'utc_timestamp': 'Date'}, inplace=True)
df['Date'] = df['Date'].dt.tz_convert('Europe/Stockholm').dt.tz_localize(None)
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
print(df.columns)
df.drop(columns=['cet_cest_timestamp', 'SE_load_forecast_entsoe_transparency', 'SE_1_load_forecast_entsoe_transparency',
                 'SE_1_price_day_ahead', 'SE_2_price_day_ahead', 'SE_3_price_day_ahead', 'SE_4_price_day_ahead', 'SE_2_load_forecast_entsoe_transparency',
                 'SE_3_load_forecast_entsoe_transparency','SE_4_load_forecast_entsoe_transparency', 'SE_wind_offshore_capacity', 'SE_wind_onshore_capacity','SE_wind_capacity'], inplace=True)
print(df.columns)

df.to_csv(path_to_structured + filename, index=False)
