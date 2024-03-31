import pandas as pd
import os
import numpy as np


import json

cities_list = os.listdir(r"data/weather")

def get_weather_data(year,month):
    weather = []
    for city in cities_list:
        city_path = os.path.join(r"data/weather", city)
        weather_files = os.listdir(city_path)
        for weather_file in weather_files:
            
            if weather_file.endswith('.json') and (f'{year}-{month}' in weather_file):
                with open(os.path.join(city_path, weather_file)) as f:
                    data = json.load(f)
                    airport = city
                    for daily_data in data['data']['weather']:
                        date = daily_data['date']
                        for hourly_data in daily_data['hourly']:
                            weather_data = {}
                            weather_data['airport'] = airport
                            weather_data['date'] = date
                            weather_data['windSpeedKmph']= hourly_data['windspeedKmph']
                            weather_data['WindDirDegree']= hourly_data['winddirDegree']
                            weather_data['WeatherCode']= hourly_data['weatherCode']
                            weather_data['precipMM']= hourly_data['precipMM']
                            weather_data['visibility']= hourly_data['visibility']
                            weather_data['pressure']= hourly_data['pressure']
                            weather_data['cloudcover']= hourly_data['cloudcover']  
                            weather_data['DewPointF']= hourly_data['DewPointF']
                            weather_data['WindGustKmph']= hourly_data['WindGustKmph']
                            weather_data['tempF']= hourly_data['tempF']
                            weather_data['WindChillF']= hourly_data['WindChillF']
                            weather_data['humidity']= hourly_data['humidity']
                            weather_data['time']= hourly_data['time']
                            weather.append(weather_data)
    weather_df = pd.DataFrame(weather)
    weather_df['date'] = pd.to_datetime(weather_df['date'])
    weather_df['time'] = weather_df['time'].astype(np.int64) // 100
    return weather_df


if not os.path.exists("flight_data_processed"):
        os.makedirs("flight_data_processed")


files = os.listdir(r"data")

required_columns = ["FlightDate","Quarter","Year","Month","DayofMonth","DepTime","DepDel15","CRSDepTime","DepDelayMinutes","Origin","Dest","ArrTime","CRSArrTime","ArrDel15","ArrDelayMinutes"]

for file in files:
    final_data = pd.DataFrame()
    if file != 'weather':
        file_path = os.path.join(r"data", file)
        data_folders = os.listdir(file_path)
        for data_folder in data_folders:
            data_files = os.listdir(os.path.join(file_path, data_folder))
            for data_file in data_files:
                if data_file.endswith('.csv') and 'On_Time_On_Time_Performance' in data_file:
                    year = int(data_file.split('_')[5])
                    month = int(data_file.split('_')[6].split('.')[0])
                    try:
                        print(f'Reading {data_file} ...')
                        df = pd.read_csv(os.path.join(file_path, data_folder, data_file), low_memory=False)
                        df = df[required_columns]
                        df['FlightDate'] = pd.to_datetime(df['FlightDate'])
                        df['time'] = df['DepTime'].fillna(0).astype(np.int64) // 100
                        weather_data = get_weather_data(year, month)
                        
                        mergerd_data = pd.merge(df, weather_data, how='left', left_on=['Origin', 'time', 'FlightDate'], right_on=['airport', 'time', 'date'])
                        mergerd_data = pd.merge(mergerd_data, weather_data, how='left', left_on=['Dest', 'time', 'FlightDate'], right_on=['airport', 'time', 'date'])
                        # mergerd_data.to_csv(os.path.join(r"flight_data_processed", data_file), index=False)
                        final_data = pd.concat([final_data, mergerd_data], ignore_index=True)
                        print(f'Finished reading {data_file}')
                    except Exception as e:
                        print(f'Error reading {data_file} : {e}')


    final_data.to_csv(f'flight_data_{file}.csv', index=False)                   
    print(f"Shape of flight data in {file}",final_data.shape)
    print(f"Head of flight data in {file}" ,final_data.head())



