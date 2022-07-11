import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['figure.dpi'] = 150
# pd.options.display.max_rows = 20

# prices_data = pd.read_csv("prices.txt", nrows = 5, delim_whitespace = True, header = None)
prices_data = pd.read_csv("prices.txt", delim_whitespace = True, header = None)
prices_data[0].plot()
# prices_data[1].plot()
prices_data[55].plot()

plt.show()

# prices_data

# prices_data[0].plot()
# prices_data[1].plot()

# x_values = [1, 2, 3, 4]
# y_values = [6, 5, 4, 3]
# plt.scatter(x_values, y_values)


nInst = 100
currentPos = np.zeros(nInst) # array of 100 zeros

def getMyPosition (prcSoFar):
    global currentPos

    # Build your function body here

    return currentPos

    
