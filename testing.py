import pandas as pd
from sklearn.feature_selection import SelectKBest
import requests

# jan_data = pd.read_csv("January_2019.csv")
# dec_data = pd.read_csv("December_2018.csv")
# feb_data = pd.read_csv("February_2019.csv")
#
# n_samples = 500
#
# c0_dec = jan_data.where(jan_data["ARR_DEL15"]==0).__len__()
# c1_dec = jan_data.where(jan_data["ARR_DEL15"]==1).__len__()
#
# c0_jan = jan_data.where(jan_data["ARR_DEL15"]==0).__len__()
# c1_jan = jan_data.where(jan_data["ARR_DEL15"]==1).__len__()
#
# c0_feb = jan_data.where(jan_data["ARR_DEL15"]==0).__len__()
# c1_feb = jan_data.where(jan_data["ARR_DEL15"]==1).__len__()
#
# print(c0_dec,c1_dec,c0_jan,c1_jan,c0_feb,c1_feb)
# jan_c0 = jan_data.where(jan_data["ARR_DEL15"]==0).sample(frac=n_samples/c0_jan)
# jan_c1 = jan_data.where(jan_data["ARR_DEL15"]==1).sample(frac=n_samples/c1_jan)
# # print(jan_c0)
# jan_min= pd.concat([jan_c0,jan_c1])
#
# feb_min= pd.concat([feb_data.where(feb_data["ARR_DEL15"]==0).sample(frac=n_samples/c0_feb),feb_data.where(feb_data["ARR_DEL15"]==1).sample(frac=n_samples/c1_feb)])
# dec_min= pd.concat([dec_data.where(dec_data["ARR_DEL15"]==0).sample(frac=n_samples/c0_dec),dec_data.where(dec_data["ARR_DEL15"]==1).sample(frac=n_samples/c1_dec)])
#
# minimized_data = pd.concat([dec_min,jan_min,feb_min])
#
# minimized_data.to_csv("minimized_data.csv")



data = pd.read_csv("minimized_data.csv")
print(data["ARR_DEL15"].value_counts())






# r = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history?aggregateHours=1&combinationMethod=aggregate&startDateTime=2021-01-25T00%3A00%3A00&endDateTime=2021-01-26T00%3A00%3A00&dayEndTime=13%3A0%3A0&maxStations=-1&maxDistance=-1&contentType=csv&unitGroup=metric&locationMode=array&key=X4W2VQL5SYLDFWQHHV22U84UH&dataElements=default&locations=London%7CDetroit")
# print(r.text)