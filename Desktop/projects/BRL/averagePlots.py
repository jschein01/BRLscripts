import pandas as pd
import pathlib as pl
import matplotlib.pyplot as plt
import numpy as np
import os
import random

syncedDataPath = "C:\\Users\\jared\\Desktop\\projects\\BRL\\syncedData"
syncedDataPath = pl.Path(syncedDataPath)
avgDf = pd.DataFrame()

for dir in syncedDataPath.glob('*/'):
    for files in dir.glob('*.csv'):
        df = pd.read_csv(files, dtype=np.float64, header=None, skiprows=1)
        df = df[df.columns[1]]
        df = df[60:120]  # Adjusted start index for ringdown
        avgDf = pd.concat([avgDf, df], axis=1)  # Concatenate dataframes

    avgDf = avgDf.mean(axis=1) # Average the data


    avgDf.plot(label=dir.stem, ylim=(-0.02, 0.02))
plt.title('Average Ringdown Pulse')
plt.xlabel('Index')
plt.ylabel('Voltage')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()  