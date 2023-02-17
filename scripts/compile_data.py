import pandas as pd
import os

filename = 'all_data.csv'
path_to_structured = '../data/Structured/'

if os.path.exists(path_to_structured + filename):
    os.remove(path_to_structured + filename)

df = pd.DataFrame(pd.date_range(start='1/1/2000',
                                end='12/31/2022', freq='H'), columns=['Date'])
data = os.listdir(path_to_structured)
for i in data:
    if 'data' in i:
        continue
    print(i)
    df2 = pd.read_csv(path_to_structured + i, sep=',',
                      parse_dates=['Date'])
    df2['Date'] = pd.to_datetime(df2['Date'], format='%Y-%m-%d %H:%M:%S')
    print(df2.head())
    df = pd.merge(df, df2, on='Date', how='left')
df = df.sort_values(by=['Date'])
# df.drop(df.tail(100000).index,
#         inplace=True)
print(df.shape)
df.to_csv(path_to_structured + filename, index=False)
