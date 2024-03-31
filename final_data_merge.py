import os
import pandas as pd

# if not os.path.exists("flight_data_processed"):
#         os.makedirs("flight_data_processed")

weather_data = pd.DataFrame()

files = os.listdir(r"weather_data_processed")
for file in files:
    try:
        df = pd.read_csv(os.path.join(r"weather_data_processed", file), low_memory=False)
        weather_data = pd.concat([weather_data, df], ignore_index=True)
    except Exception as e:
        print(f'Error reading {file} : {e}')

flight_data = pd.read_csv('flight_data.csv', low_memory=False)
# print(flight_data.shape)

flight_data['time'] = flight_data['DepTime']//100
weather_data['time'] = weather_data['time']//100
weather_data['date'] = pd.to_datetime(weather_data['date'])
flight_data['FlightDate'] = pd.to_datetime(flight_data['FlightDate'])

flight_data = pd.merge(flight_data, weather_data, how='left', left_on=['Origin', 'FlightDate', 'time'], right_on=['airport', 'date', 'time'])
flight_data = pd.merge(flight_data, weather_data, how='left', left_on=['Dest', 'FlightDate', 'time'], right_on=['airport', 'date', 'time'])

flight_data.to_csv('merged_data.csv', index=False)