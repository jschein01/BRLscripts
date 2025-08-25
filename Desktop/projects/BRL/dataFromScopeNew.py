import pandas as pd
import pathlib as pl
import matplotlib.pyplot as plt
import numpy as np
import os
threshold = 0.05

"This is a python script to sync data from multiple csv files in a directory based on a voltage threshold and save the synced data to a specified directory."
"It also has an option to plot the synced data."


def main():
    print(f"Please input dir path:")
    dataPath = input()
    dataPath = pl.Path(dataPath)
    print(f"Please input save path:")   
    savePath = input()
    savePath = pl.Path(savePath)
    for dir in dataPath.glob('*/'):
        sync_data(dir, savePath=savePath, threshold=threshold)
    print("Data syncing complete. Would you like to plot the trials? (y/n)")
    userInput = input().lower()
    if userInput == 'y':
        plot_trials(windowSize=75, data=None, plot=True)
    else:
        print("Skipping plotting trials.")


def grab_data(fileName):
    data = pd.read_csv(fileName, dtype=np.float64, header=None, skiprows=12)
    data = data.dropna(axis=1, how='all')  # Drop columns with all NaN values
    data = data.dropna(axis=0, how='all')  # Drop rows with all NaN values
    # data = data.rolling(window=1, min_periods=1).mean()  # Apply rolling mean with a window size of 2
    return data


def sync_data(dir, savePath, threshold=threshold):
    index = 0
    for files in os.listdir(dir):
        if files.endswith('.csv'):
            filePath = os.path.join(dir, files)
            data=grab_data(filePath)
            time = data[data.columns[0]]
            voltage = data[data.columns[1]]
            for voltages in voltage:
                if voltages > threshold:
                    index = voltage.index[voltage == voltages][0]
                    voltage = voltage[index:]
                    time = time[index:]
                    save_data_portion(time, voltage, 0, len(voltage), f'synced_{files}', savePath)
                    print(f"Data synced and saved for {files} starting from index {index}.")
                    break



def save_data_portion(timeCol, voltCol, start, end, fileName, savePath):
    """
    Saves a portion of the data from start to end indices to a CSV file.
    """
    fileDest = savePath
    fileName = os.path.join(fileDest, fileName ) # Ensure the file name is unique
    volt_data = voltCol[start:end]
    time_data = timeCol[start:end]
    data_portion = pd.concat([time_data, volt_data], axis=1)
    data_portion.to_csv(fileName, index=False, header=['Time', 'Voltage'])
    print(f"Data portion saved to {fileName}")

def plot_trials(windowSize=75, data=None, plot=True):

    timeCol= data[data.columns[0]] #time
    voltCol = data[data.columns[1]]  # Get the second column voltage
    voltCol = voltCol.dropna()  # Drop NaN values from the second column
    timeCol = timeCol.dropna()  # Drop NaN values from the first column
        
    maxVal = voltCol[0:].max()  # Get the maximum value from the second column
    maxIndex = voltCol[0:].index[voltCol[0:] == maxVal][0]  # Get the index of the maximum value

    startIndex = maxIndex - windowSize
    endIndex = maxIndex + windowSize*2
    plt.figure(figsize=(10, 5))
    
    voltCol.plot(x=voltCol, y=timeCol, xlim=(startIndex, endIndex), ylim=(-0.02, maxVal*1.1), title=f'Trial- Voltage vs Time')