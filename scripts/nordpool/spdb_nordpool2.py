import pandas as pd
import os

filename = 'spbc_nordpool2.csv'
path_to_raw = '../../data/Raw/nordpool/System_price_bid_curves/'
path_to_structured = '../../data/Structured/'


if os.path.exists(path_to_structured + filename):
    os.remove(path_to_structured + filename)
years = os.listdir(path_to_raw)
for i in years:

    if int(i) < 2018:
        continue
    if int(i) < 2018:
        print(i)
        months = os.listdir(path_to_raw + '/' + i)
        for j in months:
            files = os.listdir(path_to_raw + i + '/' + j)
            for f in files:
                print(f)
                # Import data from sdv file
                dfRaw = pd.read_excel(
                    path_to_raw + i + '/' + j + '/' + f, nrows=12)
                dfRaw = dfRaw[2:]
                dfRaw = dfRaw.reindex(sorted(dfRaw.columns), axis=1)
                names = dfRaw.iloc[0:12, -1]
                try:
                    end_index = names.to_list().index('Buy curve')
                    names = names[0:end_index]
                except:
                    names
                if names.shape[0] > 0:
                    dfRaw['names'] = names
                    cols = [col for col in dfRaw.columns if 'Bid' in col]
                    dfRaw.drop(cols, axis=1, inplace=True)
                    dfRaw.dropna(inplace=True)
                    df = pd.melt(dfRaw, id_vars=['names'],
                                 value_vars=dfRaw.columns, var_name='Date', value_name='Values')
                    df['Date'] = df['Date'].str.slice(0, 19)
                    df['Date'] = pd.to_datetime(
                        df['Date'], format='%d.%m.%Y %H:%M:%S')
                    # if df['Date'][1] < pd.to_datetime('2010-10-30'):
                    #     continue
                    # print(df.iloc[:, 0:2].head(10))
                    # print(df.columns)
                    # print(df.iloc[:, 0:2].duplicated().sum())
                    # print(df.iloc[:, 0:2].duplicated().index)
                    # for row in df.itertuples():
                    #     print(row)
                    # print(df.shsape)
                    df.drop(df[df.iloc[:, 0:2].duplicated()].index,
                            inplace=True)
                    # df = df.drop_duplicates()
                    df = df.pivot(index='Date', columns='names',
                                  values='Values')
                    if(df.shape[1] < 9):
                        columns = df.columns.tolist()
                        for x in range(9 - df.shape[1]):
                            columns.append(str(x))
                        df = df.reindex(columns=list(columns))
                    df.to_csv(path_to_structured + filename, index=True, mode='a',
                              header=not os.path.exists(path_to_structured + filename))

    else:
        files = os.listdir(path_to_raw + i)
        for f in files:
            print(f)
            # Import data from sdv file
            dfRaw = pd.read_excel(
                path_to_raw + i + '/' + f, nrows=12)
            dfRaw = dfRaw[2:]
            dfRaw = dfRaw.reindex(sorted(dfRaw.columns), axis=1)
            names = dfRaw.iloc[0:12, -1]
            try:
                end_index = names.to_list().index('Buy curve')
                names = names[0:end_index]
            except:
                names
            if names.shape[0] > 0:
                dfRaw['names'] = names
                cols = [col for col in dfRaw.columns if 'Bid' in col]
                dfRaw.drop(cols, axis=1, inplace=True)
                dfRaw.dropna(inplace=True)
                df = pd.melt(dfRaw, id_vars=['names'],
                             value_vars=dfRaw.columns, var_name='Date', value_name='Values')
                df['Date'] = df['Date'].str.slice(0, 19)
                df['Date'] = pd.to_datetime(
                    df['Date'], format='%d.%m.%Y %H:%M:%S')
                df.drop(df[df.iloc[:, 0:2].duplicated()].index,
                        inplace=True)
                # df = df.drop_duplicates()
                df = df.pivot(index='Date', columns='names', values='Values')
                if(df.shape[1] < 9):
                    columns = df.columns.tolist()
                    for x in range(9 - df.shape[1]):
                        columns.append(str(x))
                    df = df.reindex(columns=list(columns))
                df.to_csv(path_to_structured + filename, index=True, mode='a',
                          header=not os.path.exists(path_to_structured + filename))
