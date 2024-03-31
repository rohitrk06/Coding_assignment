import pandas as pd 
import os
import numpy as np


import json

cities_list = os.listdir(r"data/weather")
# print(cities_list)

if not os.path.exists("weather_data_processed"):
        os.makedirs("weather_data_processed")

for city in cities_list:
    city_path = os.path.join(r"data/weather", city)
    weather_files = os.listdir(city_path)
    
    for weather_file in weather_files:
        weather = []
        if weather_file.endswith('.json') and ('2016' in weather_file or '2017' in weather_file):
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
        weather_df.to_csv(f'weather_data_processed/{city}.csv', index=False)