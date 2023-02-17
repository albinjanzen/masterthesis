import pandas as pd
import os

filename = 'spbc_nordpool.csv'
path_to_raw = '../../data/Raw/nordpool/System_price_bid_curves/'
path_to_structured = '../../data/Structured/'


if os.path.exists(path_to_structured + filename):
    os.remove(path_to_structured + filename)
years = os.listdir(path_to_raw)
for i in years:
    print(i)
    if int(i) < 2018:
        months = os.listdir(path_to_raw + '/' + i)
        for j in months:
            files = os.listdir(path_to_raw + i + '/' + j)
            for f in files:
                # Import data from sdv file
                dfRaw = pd.read_excel(path_to_raw + i + '/' + j + '/' + f)
                names = dfRaw.iloc[0:12, 0]
                names.drop([5], inplace=True)
                dfRaw = dfRaw.reindex(sorted(dfRaw.columns), axis=1)
                dfRaw = dfRaw.iloc[:, 0:24]
                dfRaw = dfRaw[2:12]
                dfRaw.drop([5], inplace=True)
                dfRaw['names'] = names
                df = pd.melt(dfRaw, id_vars=['names'],
                             value_vars=dfRaw.columns, var_name='Date', value_name='Value')
                df = df.pivot(index='Date', columns='names', values='Value')
                df.index = df.index.map(lambda x: x.rstrip(' +'))
                try:
                    df.index = pd.to_datetime(df.index)
                except:
                    for c in df.columns:
                        try:
                            pd.to_datetime(df[c])
                        except:
                            df.drop(c, axis=1, inplace=True)

                df.to_csv(path_to_structured + filename, index=True, mode='a',
                          header=not os.path.exists(path_to_structured + filename))
    else:
        files = os.listdir(path_to_raw + i)
        for f in files:
            # Import data from sdv file
            dfRaw = pd.read_excel(path_to_raw + i + '/' + f)
            names = dfRaw.iloc[0:12, 0]
            names.drop([5], inplace=True)
            dfRaw = dfRaw.reindex(sorted(dfRaw.columns), axis=1)
            dfRaw = dfRaw.iloc[:, 0:24]
            if pd.to_datetime(dfRaw.columns[1], dayfirst=True) < pd.to_datetime('2022-03-16'):
                dfRaw = dfRaw[2:12]
                dfRaw.drop([5], inplace=True)
            else:
                dfRaw = dfRaw[2:5]
            dfRaw['names'] = names
            df = pd.melt(dfRaw, id_vars=['names'],
                         value_vars=dfRaw.columns, var_name='Date', value_name='Value')
            df = df.pivot(index='Date', columns='names', values='Value')
            df.index = df.index.map(lambda x: x.rstrip(' +'))
            try:
                df.index = pd.to_datetime(df.index, dayfirst=True)
            except:
                for c in df.columns:
                    try:
                        pd.to_datetime(df[c], dayfirst=True)
                    except:
                        df.drop(c, axis=1, inplace=True)
            df.to_csv(path_to_structured + filename, index=True, mode='a',
                      header=not os.path.exists(path_to_structured + filename))
