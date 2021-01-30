import pandas as pd
import requests
import numpy as np
from urllib.parse import quote_plus
import json

apikeys = ("X4W2VQL5SYLDFWQHHV22U84UH","5MEK2QULQADQ8LEZYRLKW5WRR","9WM3JS3RCT2UXA74PPERUSMUM","V8MZB5V25LFTR7BTSKB9KZ7PA","B9EZWGFM25ZMCF66VWRLS4ZXW","W7CJZTC9VPA2P8NGM3HJQ9PSY","AY5PK59M7R9ZJ7WVCAWY8YF9T","SMUGLD75W4FKCZAG2B3A6MBC8")


# jan_data = pd.read_csv("January_2019.csv").drop(columns=["Unnamed: 91"]).dropna(how='all')
# dec_data = pd.read_csv("December_2018.csv").drop(columns=["Unnamed: 91"]).dropna(how='all')
# feb_data = pd.read_csv("February_2019.csv").drop(columns=["Unnamed: 91"]).dropna(how='all')
# jan_data = jan_data[jan_data["ARR_DEL15"].notna()]
# dec_data = dec_data[dec_data["ARR_DEL15"].notna()]
# feb_data = feb_data[feb_data["ARR_DEL15"].notna()]
#
# print("Missing output January:"+str(jan_data["ARR_DEL15"].isna().any()))
# print("Missing output February:"+str(feb_data["ARR_DEL15"].isna().any()))
# print("Missing output December:"+str(dec_data["ARR_DEL15"].isna().any()))
# n_samples = 500
#
# c0_dec_count = dec_data[dec_data["ARR_DEL15"]==0].__len__()
# c1_dec_count = dec_data[dec_data["ARR_DEL15"]==1].__len__()
#
#
# c0_jan_count = jan_data[jan_data["ARR_DEL15"]==0].__len__()
# c1_jan_count = jan_data[jan_data["ARR_DEL15"]==1].__len__()
#
# c0_feb_count = feb_data[feb_data["ARR_DEL15"]==0].__len__()
# c1_feb_count = feb_data[feb_data["ARR_DEL15"]==1].__len__()
#
# print(c0_dec_count,c1_dec_count,c0_jan_count,c1_jan_count,c0_feb_count,c1_feb_count)
#
# jan_c0 = jan_data[jan_data["ARR_DEL15"]==0]
# jan_c0 =  jan_c0.sample(frac=n_samples/c0_jan_count,random_state=1)
# jan_c1 = jan_data[jan_data["ARR_DEL15"]==1]
# jan_c1 = jan_c1.sample(frac=n_samples/c1_jan_count,random_state=1)
# # print(jan_c0)
# jan_min= pd.concat([jan_c0,jan_c1])
#
# feb_c0 = feb_data[feb_data["ARR_DEL15"]==0].sample(frac=n_samples/c0_feb_count,random_state=1)
# feb_c1 = feb_data[feb_data["ARR_DEL15"]==1].sample(frac=n_samples/c1_feb_count,random_state=1)
# feb_min= pd.concat([feb_c0,feb_c1])
#
# dec_c0 = dec_data[dec_data["ARR_DEL15"]==0].sample(frac=n_samples/c0_dec_count,random_state=1)
# dec_c1 = dec_data[dec_data["ARR_DEL15"]==1].sample(frac=n_samples/c1_dec_count,random_state=1)
# dec_min= pd.concat([dec_c0,dec_c1])
#
# minimized_data = pd.concat([dec_min,jan_min,feb_min])
#
#
#
# minimized_data = minimized_data.dropna(axis=1, how="all") #se otstranuvaat praznite koloni
#
# #Se zima primer request samo da se izvadat iminjata na kolonite
# resp = json.loads(requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history?aggregateHours=1&combinationMethod=aggregate&startDateTime=2021-01-01T00%3A00%3A00&endDateTime=2021-01-01T00%3A00%3A00&dayEndTime=12%3A58%3A0&maxStations=-1&maxDistance=-1&contentType=json&unitGroup=metric&locationMode=single&key=X4W2VQL5SYLDFWQHHV22U84UH&dataElements=default&locations=Tampa%20%2CFL").content)
# col_names = []
# for col_id in resp["columns"].keys():
#     col_names.append(resp["columns"][col_id]["name"])
# for col_name in col_names:
#     minimized_data["Departure "+col_name]=np.nan
# for col_name in col_names:
#     minimized_data["Arrival "+col_name]=np.nan
#
# #     #se dodavaat novite koloni posebno za departure, posebno za arrival
# minimized_data.to_csv("minimized_data.csv")

minimized_data = pd.read_csv("minimized_data.csv").drop(columns=["Unnamed: 0"])
data = minimized_data.values
dep_start_idx = minimized_data.columns.to_list().index("Departure Temperature")
arr_start_idx = minimized_data.columns.to_list().index("Arrival Temperature")
try:
    for ap_k in apikeys:
        for (row_id,row) in enumerate(data):
            year = row[0]
            month = row[1]
            day = row[2]
            origin_city = row[7]
            dest_city = row[10]
            dep_time = row[17][:4]
            arr_time = row[28][:4]
            #popolnuvame departure vremenski podatoci
            if row[dep_start_idx] is None or np.isnan(row[dep_start_idx]):
                base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history?aggregateHours=1&combinationMethod=aggregate"
                query = "&startDateTime="+str(year)+"-"+str(month).zfill(2)+"-"+str(day).zfill(2)+"T00:00:00"
                query += "&endDateTime=" + str(year) + "-"+str(month).zfill(2)+"-"+str(day).zfill(2)+ "T00:00:00"
                query += "&dayStartTime="+dep_time[:2]+":"+dep_time[2:]+":0"
                query += "&dayEndTime=" + dep_time[:2] +":59:0"
                query += "&maxStations=-1&maxDistance=-1&contentType=json&unitGroup=metric&locationMode=single"
                query += "&key="+ap_k+"&dataElements=default"
                query += "&locations="+origin_city
                result = json.loads(requests.get(base_url+quote_plus(query,safe="=&")).content)

                if "remainingCost" not in result.keys():
                    break

                values = result["location"]["values"][0]
                for (i,key) in enumerate(values.keys()):
                    row[dep_start_idx+i] = values[key]

            #Popolnuvame prazni arrival vremenski podatoci
            if row[arr_start_idx] is None or np.isnan(row[arr_start_idx]):
                base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history?aggregateHours=1&combinationMethod=aggregate"
                query = "&startDateTime=" + str(year) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2) + "T00:00:00"
                query += "&endDateTime=" + str(year) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2) + "T00:00:00"
                query += "&dayStartTime=" + arr_time[:2] + ":" + arr_time[2:] + ":0"
                query += "&dayEndTime=" + arr_time[:2] + ":59:0"
                query += "&maxStations=-1&maxDistance=-1&contentType=json&unitGroup=metric&locationMode=single"
                query += "&key=" + ap_k + "&dataElements=default"
                query += "&locations=" + dest_city
                result = json.loads(requests.get(base_url + quote_plus(query, safe="=&")).content)
                if "remainingCost" not in result.keys():
                    break
                values = result["location"]["values"][0]
                for (i, key) in enumerate(values.keys()):
                    row[arr_start_idx + i] = values[key]

            if row_id==2999:
                raise Exception("Done!")

finally:
    new_minimized_data = pd.DataFrame(data,columns=minimized_data.columns)
    print()
    new_minimized_data.to_csv("minimized_data.csv")
