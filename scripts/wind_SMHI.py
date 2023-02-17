import requests
import pandas as pd
import os
import csv

filename = 'wind.csv'
path_to_raw = '../data/Raw/SMHI/rain/'
path_to_structured = '../data/Structured/'

stations = [52350, 74460, 95130, 146050, 180940]
df = pd.DataFrame(pd.date_range(start='1/1/2000',
                                end='12/31/2022', freq='H'), columns=['Date'])
print(df.head())
for station in stations:
    response = requests.get(
        'https://opendata-download-metobs.smhi.se/api/version/latest/parameter/4/station/' + str(station) + '/period/corrected-archive/data.csv')
    pd.DataFrame(response.text.splitlines()).to_csv(path_to_raw +
                                                    str(station)+'.csv', index=False)

if os.path.exists(path_to_structured + filename):
    os.remove(path_to_structured + filename)

for station in stations:
    Header_Row = 0
    with open(path_to_raw + str(station)+'.csv') as file:
        reader = csv.reader(file, delimiter=';')
        for line in reader:  # Iterates through the rows of your csv
            if 'Datum' in line:  # If the string you want to search is in the row
                Header_Row = reader.line_num
                break
    temporary = pd.read_csv(path_to_raw + str(station)+'.csv', sep=';',
                            skiprows=Header_Row-1)
    temporary = temporary.iloc[:, 0:3]
    temporary['Date'] = pd.to_datetime(
        temporary['Datum'] + ' ' + temporary['Tid (UTC)'], format='%Y-%m-%d %H:%M:%S')
    temporary.rename(
        columns={'Vindhastighet': str(station)+'_wind'}, inplace=True)
    temporary.rename(columns={'Kvalitet': str(
        station)+'_quality'}, inplace=True)
    temporary.drop(['Datum', 'Tid (UTC)'], axis=1, inplace=True)
    temporary = temporary[~(temporary['Date'] < '2000-01-01')]
    df = pd.merge(df, temporary, on='Date', how='outer')
    df.sort_values(by=['Date'], inplace=True)
df.to_csv(path_to_structured + filename, index=False)
