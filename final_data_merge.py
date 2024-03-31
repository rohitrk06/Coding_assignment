import os
import pandas as pd

if not os.path.exists("flight_data_processed"):
        os.makedirs("flight_data_processed")

# def read_weather_data(filename):
#     parse_dates = ['date']
#     dtype = {'time': int}
#     return pd.read_csv(filename, parse_dates=parse_dates, dtype=dtype)

# Function to merge flight data with weather data
# def merge_flight_weather(flight_data, weather_data, airport_column, date_column, time_column):
#     merged_flight_data = pd.merge(flight_data, weather_data, how='left', left_on=[airport_column, 'FlightDate', time_column],
#                                   right_on=['airport', date_column, time_column])
#     return merged_flight_data

# Paths
# flight_data_path = 'flight_data.csv'
weather_data_dir = 'weather_data_processed'
merged_data_path = 'merged_data.csv'

# Read flight data
# flight_data = read_flight_data(flight_data_path)

# Initialize an empty DataFrame for weather data
weather_data = pd.DataFrame()

# Read weather data files and concatenate
for file in os.listdir(weather_data_dir):
    try:
        df = pd.read_csv(os.path.join(weather_data_dir, file), low_memory=False)
        weather_data = pd.concat([weather_data, df], ignore_index=True)
    except Exception as e:
        print(f'Error reading {file} : {e}')

weather_data['time'] = weather_data['time'] // 100
weather_data['date'] = pd.to_datetime(weather_data['date'])

print(weather_data.info())

# Function to read weather data with specified data types and date parsing


files = os.listdir(r"data")

req_flight_data_columns = ["FlightDate","Quarter","Year","Month","DayofMonth","DepTime","DepDel15","CRSDepTime","DepDelayMinutes","Origin","Dest","ArrTime","CRSArrTime","ArrDel15","ArrDelayMinutes"]

for file in files:
    if file != 'weather':
        file_path = os.path.join(r"data", file)
        data_folders = os.listdir(file_path)
        for data_folder in data_folders:
            data_files = os.listdir(os.path.join(file_path, data_folder))
            for data_file in data_files:
                if data_file.endswith('.csv') and 'On_Time_On_Time_Performance' in data_file:
                    try:
                        print(f' {"#" * 5} Reading {data_file} {"#" * 5}')
                        df = pd.read_csv(os.path.join(file_path, data_folder, data_file), low_memory=False)
                        df = df[req_flight_data_columns]
                        # final_data = pd.concat([final_data, df], ignore_index=True)
                        print(f'Finished reading {data_file}')
                    except Exception as e:
                        print(f'Error reading {data_file} : {e}')

                    df['time'] = df['DepTime'] // 100
                    df['FlightDate'] = pd.to_datetime(df['FlightDate'])
                    print(df.info())
                    print(df['time'])
                    print(weather_data['time'])
                    df = pd.merge(df, weather_data, how='left', left_on=['Origin'], right_on=['airport'])
                    # print(df.head())
                    df = pd.merge(df, weather_data, how='inner', left_on=['Dest'], right_on=['airport'])
                    # print(df.head())
                    df.to_csv(os.path.join(r"flight_data_processed", data_file), index=False)
                break
            break
    break



# flight_data['time'] = flight_data['DepTime'] // 100
# weather_data['time'] = weather_data['time'] // 100
# weather_data['date'] = pd.to_datetime(weather_data['date'])
# flight_data['FlightDate'] = pd.to_datetime(flight_data['FlightDate'])

# flight_data = merge_flight_weather(flight_data, weather_data, 'Origin', 'date', 'time')
# flight_data = merge_flight_weather(flight_data, weather_data, 'Dest', 'date', 'time')

# flight_data.to_csv(merged_data_path, index=False)



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