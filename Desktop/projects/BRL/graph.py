import pandas as pd
import pathlib as pl
import matplotlib.pyplot as plt
import numpy as np

print(f"Please enter file path:")
filePath = input().strip()
print(f"How many plots?")
numPlots = input().strip()
print(f"Plot whole pulse or ringdown? (p/r)")
inputType = input().strip().lower()
path = pl.Path(filePath)
fig = plt.figure(figsize=(10, 5))


def plot_data(inputType):
    x = 0
    startIndex = 0
    if inputType == 'r':
        startIndex = 50
    for files in path.glob('*.csv'):
        if x >= int(numPlots):
            break
        df = pd.read_csv(files, dtype=np.float64, header=None, skiprows=1)
        df = df[df.columns[1]]
        df = df[startIndex]
        df.plot(label=files.stem)
        x += 1

plot_data(inputType)


plt.title('Outputs')
plt.xlabel('Index')
plt.ylabel('Voltage')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()