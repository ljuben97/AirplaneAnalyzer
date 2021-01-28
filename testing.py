import pandas as pd
from sklearn.feature_selection import SelectKBest
import requests
import numpy as np

jan_data = pd.read_csv("January_2019.csv").drop(columns=["Unnamed: 91"])
dec_data = pd.read_csv("December_2018.csv").drop(columns=["Unnamed: 91"])
feb_data = pd.read_csv("February_2019.csv").drop(columns=["Unnamed: 91"])
jan_data = jan_data[jan_data["ARR_DEL15"].notna()]
dec_data = dec_data[dec_data["ARR_DEL15"].notna()]
feb_data = feb_data[feb_data["ARR_DEL15"].notna()]

print("Missing output January:"+str(jan_data["ARR_DEL15"].isna().any()))
print("Missing output February:"+str(feb_data["ARR_DEL15"].isna().any()))
print("Missing output December:"+str(dec_data["ARR_DEL15"].isna().any()))
n_samples = 500

c0_dec_count = jan_data.where(jan_data["ARR_DEL15"]==0).__len__()
c1_dec_count = jan_data.where(jan_data["ARR_DEL15"]==1).__len__()


c0_jan_count = jan_data.where(jan_data["ARR_DEL15"]==0).__len__()
c1_jan_count = jan_data.where(jan_data["ARR_DEL15"]==1).__len__()

c0_feb_count = jan_data.where(jan_data["ARR_DEL15"]==0).__len__()
c1_feb_count = jan_data.where(jan_data["ARR_DEL15"]==1).__len__()

print(c0_dec_count,c1_dec_count,c0_jan_count,c1_jan_count,c0_feb_count,c1_feb_count)
jan_c0 = jan_data.where(jan_data["ARR_DEL15"]==0).sample(frac=n_samples/c0_jan_count,random_state=1)
jan_c1 = jan_data.where(jan_data["ARR_DEL15"]==1).sample(frac=n_samples/c1_jan_count,random_state=1)
# print(jan_c0)
jan_min= jan_c0.append(jan_c1)

feb_c0 = feb_data.where(feb_data["ARR_DEL15"]==0).sample(frac=n_samples/c0_feb_count,random_state=1)
feb_c1 = feb_data.where(feb_data["ARR_DEL15"]==1).sample(frac=n_samples/c1_feb_count,random_state=1)
feb_min= feb_c0.append(feb_c1)

dec_c0 = dec_data.where(dec_data["ARR_DEL15"]==0).sample(frac=n_samples/c0_dec_count,random_state=1)
dec_c1 = dec_data.where(dec_data["ARR_DEL15"]==1).sample(frac=n_samples/c1_dec_count,random_state=1)
dec_min= dec_c0.append(dec_c1)

minimized_data = dec_min.append(jan_min).append(feb_min)
print(minimized_data["ARR_DEL15"].value_counts())
print(minimized_data["ARR_DEL15"].isna().any())

minimized_data.to_csv("minimized_data.csv")









# r = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history?aggregateHours=1&combinationMethod=aggregate&startDateTime=2021-01-25T00%3A00%3A00&endDateTime=2021-01-26T00%3A00%3A00&dayEndTime=13%3A0%3A0&maxStations=-1&maxDistance=-1&contentType=csv&unitGroup=metric&locationMode=array&key=X4W2VQL5SYLDFWQHHV22U84UH&dataElements=default&locations=London%7CDetroit")
# print(r.text)