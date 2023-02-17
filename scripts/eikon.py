
import pandas as pd
import os

filename = 'eikon.csv'
path_to_raw = '../data/Raw/eikon.xlsx'
path_to_structured = '../data/Structured/'


if os.path.exists(path_to_structured + filename):
    os.remove(path_to_structured + filename)

# Import data from sdv file
dfRaw = pd.read_excel(
path_to_raw)
df = dfRaw.iloc[:, 0:2]
df.columns = ['Date', 'Gas']
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d %H:%M:%S')
print(df['Date'])


df.to_csv(path_to_structured + filename, index=False)