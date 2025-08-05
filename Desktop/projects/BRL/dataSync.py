import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
threshold = 0.05


def main():
    print("Please enter file directory:")
    fileName = input()
    sync_data(fileName)

def sync_data(dir):
    index = 0
    for files in os.listdir(dir):
        if files.endswith('.csv'):
            filePath = os.path.join(dir, files)
            data = pd.read_csv(filePath, dtype=np.float64, header=None, skiprows=1)
            time = data[data.columns[0]]
            voltage = data[data.columns[1]]
            for voltages in voltage:
                if voltages > threshold:
                    index = voltage.index[voltage == voltages][0]
                    voltage = voltage[index:]
                    time = time[index:]
                    save_data_portion(time, voltage, 0, len(voltage), f'synced_{files}')
                    print(f"Data synced and saved for {files} starting from index {index}.")
                    break


def save_data_portion(timeCol, voltCol, start, end, fileName):
    """
    Saves a portion of the data from start to end indices to a CSV file.
    """
    fileDest = "C:\\Users\\jared\\Desktop\\projects\\BRL\\syncedFinger"
    fileName = os.path.join(fileDest, fileName ) # Ensure the file name is unique
    volt_data = voltCol[start:end]
    time_data = timeCol[start:end]
    data_portion = pd.concat([time_data, volt_data], axis=1)
    data_portion.to_csv(fileName, index=False, header=['Time', 'Voltage'])
    print(f"Data portion saved to {fileName}")


main()


