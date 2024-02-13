import pandas as pd

def clean_data(csv_path):

    # Read csv file and read 'Null' and '' as NaN
    df = pd.read_csv(csv_path, na_values=['Null', ''])

    # Replace NaN with the previous non-null, non-empty value
    df['Value'] = df['Value'].fillna(method='ffill')

    # Convert the 'Value' column to integers
    df['Value'] = df['Value'].astype('Int64')

    return df

def calculate_total_downtime(csv_path):
    data = clean_data(csv_path)

    total_downtime = 0
    start_time = None

    for index, row in data.iterrows():
        unix_epoch, value = row['Epoch Time'], row['Value']
        if value == 1:  # Device network is down
            if start_time is None:
                start_time = unix_epoch
        else:  # Device network is up
            if start_time is not None:
                total_downtime += unix_epoch - start_time
                start_time = None

    # Add total_downtime if in the last record the device is down
    if start_time is not None:
        total_downtime += unix_epoch - start_time

    return total_downtime // 1000  # Convert milliseconds to seconds

if __name__ == "__main__":
    total_downtime = calculate_total_downtime("device_network_data.csv")

    print(f"Total Downtime: {total_downtime} seconds")

