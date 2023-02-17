import pandas as pd
import os

filename = 'nordpool_external_capacities.csv'
path_to_raw = '../../data/Raw/nordpool/External_capacities/'
path_to_structured = '../../data/Structured/'


date_df = pd.DataFrame()


if os.path.exists(path_to_structured + filename):
    os.remove(path_to_structured + filename)
years = os.listdir(path_to_raw)
for i in years:
    print(i)
    files = os.listdir(path_to_raw + i)

    for f in files:
        # Import data from sdv file
        dfRaw = pd.read_csv(path_to_raw + i + '/' + f, sep=';', skiprows=7, header=None, names=[
            'Data type',
            'Code',
            'Year',
            'Week',
            'Day',
            'Date',
            'Alias',
            '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
            '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', 'Sum'
        ], parse_dates=['Date'], dayfirst=True, encoding='unicode_escape')
        dfRaw = dfRaw.drop(dfRaw[dfRaw['Data type'] != 'UE'].index)
        dfRaw = dfRaw.drop(columns=['Year', 'Week', 'Day', 'Sum'])
        df = pd.melt(dfRaw, id_vars=['Date', 'Alias', 'Code', 'Data type'], value_vars=['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                                                                                        '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'], var_name='Hour', value_name='Value')
        df.sort_values(by=['Date', 'Hour'], inplace=True)
        # Change date format
        df['Date'] = pd.to_datetime(
            df['Date'] + ':' + df['Hour'], format='%d.%m.%Y:%H')
        # Drop variable column
        df = df.drop(columns=['Hour'])
        df = df.pivot(index='Date', values='Value', columns=[
                      'Alias', 'Code', 'Data type'])
        df.columns = ['_'.join(col).strip() for col in df.columns.values]
        date_df = pd.concat([date_df, df])
date_df.to_csv(path_to_structured + filename, index=True)
