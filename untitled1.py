# Import libraries
import json
import requests
import rdflib
from statistics import mean
import pandas as pd
import csv
# Loading data
data =  pd.read_csv(r"C:\Users\fedos\Downloads\Convertation\CH_ALL_15min_HW.csv", sep=',', encoding='unicode_escape', parse_dates=True, low_memory=False)

labels = pd.read_csv(r"C:\Users\fedos\Downloads\rt\query-result.csv", sep=',', encoding='unicode_escape', parse_dates=True, low_memory=False)

order = labels['ID']

df = data[order]

df2 = pd.DataFrame(df)
df2.columns = pd.MultiIndex.from_frame(labels)

df2.to_csv('linked.csv', index=True)

print(df2.describe())


#temp = pd.DataFrame(data, columns = ['CH_418_Temperature', 'CH_416_Temperature', 'CH_413_Temperature'])
#rh = pd.DataFrame(data, columns = ['CH_418_Humidity', 'CH_416_Humidity', 'CH_413_Humidity'])
#co2 = pd.DataFrame(data, columns = ['CH_418_CO2', 'CH_416_CO2', 'CH_413_CO2'])
#pm25 = pd.DataFrame(data, columns = ['CH_418_PM25', 'CH_416_PM25', 'CH_413_PM25'])

#print(temp.describe())
#print(rh.describe())
#print(co2.describe())
#print(pm25.describe())

#print(labels)
#df3 = pd.DataFrame(data)

#df3.columns = pd.MultiIndex.from_frame(labels)

#print(df3)
#df3.to_csv('ddf3.csv', index=True)
#print(temp)
#temp.to_csv('temp.csv', index=True)

#whats_missing(data['CH_418_Temperature'])

#whats_missing(data['CH_416_Temperature'])

#whats_missing(data['CH_413_Temperature'])

#data['CH_416_Temperature']

#data['CH_413_Temperature']


#CH_416_Temperature

#CH_413_Temperature






#for i in labels['ID']:
#    if 
    
#    print(sum(data[i])/len(data[i]))
    
    
# what_missing function helps to define missing values within the dataset
#def whats_missing(df: pd.DataFrame):
#    if df.isnull().values.any(): # check if anything is missing
 #       print("This input dataframe is missing values")
#        print(df.isnull().sum())        # Total missing values for each feature
#        print(f"Total missing values: {df.isnull().sum().sum()}")# Total missing values in the whole dataframe
#    else: print("No missing values!")
    
    # df = df.dropna(axis = 1, how='any')
# whats_missing(df)