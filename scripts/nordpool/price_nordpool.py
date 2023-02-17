import pandas as pd
import os

filename = 'price.csv'
path_to_raw = '../../data/Raw/nordpool/Elspot_file/'
path_to_structured = '../../data/Structured/'

if os.path.exists(path_to_structured + filename):
    os.remove(path_to_structured + filename)
years = os.listdir(path_to_raw)
for i in years:
    print(i)
    files = os.listdir(path_to_raw + i)

    for f in files:
        # Import data from sdv file
        dfRaw = pd.read_csv(path_to_raw + i + '/' + f, sep=';', skiprows=7, header=None, names=['Data type', 'Code', 'Year', 'Week', 'Day', 'Date', 'Alias', 'Unit', '00', '01', '02', '02B', '03',
                                                                                                '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', 'Avg/Total'], parse_dates=['Date'], dayfirst=True, encoding='unicode_escape', dtype={'int': 'S10'})
        # Select only PR data
        dfRaw = dfRaw.drop(dfRaw[dfRaw['Data type'] != 'PR'].index)
        dfRaw = dfRaw.drop(columns=['Data type',
                                    'Year', 'Week', 'Day', 'Avg/Total'])
        # Convert to long format
        df = pd.melt(dfRaw, id_vars=['Date', '02B', 'Alias', 'Unit', 'Code'], value_vars=['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                                                                                          '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'], var_name='Hour', value_name='Price')
        df.sort_values(by=['Date', 'Hour'], inplace=True)
        # Change date format
        df['Date'] = pd.to_datetime(
            df['Date'] + ':' + df['Hour'], format='%d.%m.%Y:%H')
        # Drop variable column
        df = df.drop(columns=['Hour'])
        df['Price'] = pd.to_numeric(df['Price'].str.replace(',', '.'))
        df = df[df.Unit == 'SEK']
        df = df[df.Code == 'SO']
        df = df[df.Alias.str.contains('SE')]
        df = df.drop(columns=['Unit', '02B', 'Code'])
        df = df.pivot(index='Date', columns='Alias', values='Price')
        if len(df.columns) == 1:
            df['SE1'] = df['SE']
            df['SE2'] = df['SE']
            df['SE3'] = df['SE']
            df['SE4'] = df['SE']
        if 'SE' in df.columns:
            df.drop(columns=['SE'], inplace=True, axis=1)
        df.rename(columns={'SE': 'SE_Price'}, inplace=True)
        df.to_csv(path_to_structured + filename, index=True, mode='a',
                  header=not os.path.exists(path_to_structured + filename))
