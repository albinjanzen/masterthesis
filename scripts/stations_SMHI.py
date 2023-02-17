import requests
import pandas as pd
import os
import csv

stations_list = pd.read_csv('stations.csv', sep=';', header=0)
print(stations_list)
stations_list.sort_values(
    by=['Latitud'], inplace=True, ascending=True)
print(stations_list.Id)
