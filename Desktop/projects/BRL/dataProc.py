import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    print("Please enter file path:")
    fileName = input()
    data = grab_data(fileName)
    medium = fileName
    plot_trials(windowSize=75, data=data)

def grab_data(fileName):
    data = pd.read_csv(fileName, dtype=np.float64, header=None, skiprows=10)
    data = data.dropna(axis=1, how='all')  # Drop columns with all NaN values
    data = data.dropna(axis=0, how='all')  # Drop rows with all NaN values
    # data = data.rolling(window=1, min_periods=1).mean()  # Apply rolling mean with a window size of 2

    return data

def plot_trials(windowSize=75, data=None, plot=True):
    print("How many trial? (default is 10)")
    trialNum = input()
    if trialNum.isdigit():
        trialNum = int(trialNum)
    else:
        trialNum = 10
    print("Do you want to plot the trials? (y/n)")
    userInput = input().lower()
    if userInput != 'y':
        print("Skipping plotting trials.")
        return
    print("Save Data Portion? (y/n)")
    saveInput = input().lower()
    print("What is the medium? (e.g., air, density, etc.)")
    medium = input() # Get the medium from user input
    
    
    
    for trials in range(0, 10):
        timeCol= data[data.columns[trials*2]] #time
        voltCol = data[data.columns[trials*2+1]]  # Get the second column voltage
        voltCol = voltCol.dropna()  # Drop NaN values from the second column
        timeCol = timeCol.dropna()  # Drop NaN values from the first column
        
        maxVal = voltCol[0:].max()  # Get the maximum value from the second column
        maxIndex = voltCol[0:].index[voltCol[0:] == maxVal][0]  # Get the index of the maximum value

        startIndex = maxIndex - windowSize
        endIndex = maxIndex + windowSize*2
        if saveInput == 'y':
            save_data_portion(timeCol, voltCol, startIndex, endIndex, f'trial_{trials+1}-'+medium+'-.csv')
        # Create a plot for each trial
        plt.figure(figsize=(10, 5))
    
        voltCol.plot(x=voltCol, y=timeCol, xlim=(startIndex, endIndex), ylim=(-0.02, maxVal*1.1), title=f'Trial {trials+1} - Voltage vs Time')

def save_data_portion(timeCol, voltCol, start, end, fileName):
    """
    Saves a portion of the data from start to end indices to a CSV file.
    """
    fileDest = "C:\\Users\\jared\\Desktop\\projects\\BRL"
    fileName = os.path.join(fileDest, fileName ) # Ensure the file name is unique
    volt_data = voltCol[start:end]
    time_data = timeCol[start:end]
    data_portion = pd.concat([time_data, volt_data], axis=1)
    data_portion.to_csv(fileName, index=False, header=['Time', 'Voltage'])
    print(f"Data portion saved to {fileName}")

main()


