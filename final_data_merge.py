import os
import pandas as pd

# Function to read flight data with specified data types
def read_flight_data(filename):
    dtype = {'DepTime': float}
    return pd.read_csv(filename, dtype=dtype)

# Function to read weather data with specified data types and date parsing
def read_weather_data(filename):
    parse_dates = ['date']
    dtype = {'time': int}
    return pd.read_csv(filename, parse_dates=parse_dates, dtype=dtype)

# Function to merge flight data with weather data
def merge_flight_weather(flight_data, weather_data, airport_column, date_column, time_column):
    merged_flight_data = pd.merge(flight_data, weather_data, how='left', left_on=[airport_column, 'FlightDate', time_column],
                                  right_on=['airport', date_column, time_column])
    return merged_flight_data

# Paths
flight_data_path = 'flight_data.csv'
weather_data_dir = 'weather_data_processed'
merged_data_path = 'merged_data.csv'

# Read flight data
flight_data = read_flight_data(flight_data_path)

# Initialize an empty DataFrame for weather data
weather_data = pd.DataFrame()

# Read weather data files and concatenate
for file in os.listdir(weather_data_dir):
    try:
        df = read_weather_data(os.path.join(weather_data_dir, file))
        weather_data = pd.concat([weather_data, df], ignore_index=True)
    except Exception as e:
        print(f'Error reading {file} : {e}')

# Filter weather data based on flight date and time
flight_data['time'] = flight_data['DepTime'] // 100
weather_data['time'] = weather_data['time'] // 100
weather_data['date'] = pd.to_datetime(weather_data['date'])
flight_data['FlightDate'] = pd.to_datetime(flight_data['FlightDate'])

# Merge flight data with weather data for origin and destination airports
flight_data = merge_flight_weather(flight_data, weather_data, 'Origin', 'date', 'time')
flight_data = merge_flight_weather(flight_data, weather_data, 'Dest', 'date', 'time')

# Save merged data to CSV
flight_data.to_csv(merged_data_path, index=False)



"""import os
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

flight_data.to_csv('merged_data.csv', index=False)"""