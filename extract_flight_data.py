import os
import pandas as pd

# if not os.path.exists("flight_data_processed"):
#         os.makedirs("flight_data_processed")

final_data = pd.DataFrame()

files = os.listdir(r"data")

required_columns = ["FlightDate","Quarter","Year","Month","DayofMonth","DepTime","DepDel15","CRSDepTime","DepDelayMinutes","Origin","Dest","ArrTime","CRSArrTime","ArrDel15","ArrDelayMinutes"]

for file in files:
    if file != 'weather':
        file_path = os.path.join(r"data", file)
        data_folders = os.listdir(file_path)
        for data_folder in data_folders:
            data_files = os.listdir(os.path.join(file_path, data_folder))
            for data_file in data_files:
                if data_file.endswith('.csv') and 'On_Time_On_Time_Performance' in data_file:
                    try:
                        print(f'Reading {data_file} ...')
                        df = pd.read_csv(os.path.join(file_path, data_folder, data_file), low_memory=False)
                        df = df[required_columns]
                        final_data = pd.concat([final_data, df], ignore_index=True)
                        print(f'Finished reading {data_file}')
                    except Exception as e:
                        print(f'Error reading {data_file} : {e}')

final_data.to_csv('flight_data.csv', index=False)                   
print(final_data.shape)

        
        