import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['figure.dpi'] = 150

prices_data = pd.read_csv("prices.txt", delim_whitespace = True, header = None)
prices_data.plot()
plt.show()

# prices_data

# prices_data[0].plot()
# prices_data[1].plot()

# x_values = [1, 2, 3, 4]
# y_values = [6, 5, 4, 3]
# plt.scatter(x_values, y_values)


nInst=100
currentPos = np.zeros(nInst)
NUMBER_OF_DAYS = 3

def getMyPosition (prcSoFar):
    global currentPos

    # Build your function body here

    current_day = np.shape(prcSoFar)[0]

    for i in range(nInst):
        trend = []
        stock_number = i

        #       if True, price increased, if False, price decreased
        if (current_day > NUMBER_OF_DAYS):
            for x in range(NUMBER_OF_DAYS):
                if prcSoFar[current_day - x, stock_number] - prcSoFar[current_day - x - 1, stock_number] > 0:
                    trend.append(True)
                elif prcSoFar[current_day - x, stock_number] - prcSoFar[current_day - x - 1, stock_number] < 0:
                    trend.append(False)
                else:
                    trend.append(None)

        consecutive_price_increase = True
        consecutive_price_decrease = True

        if trend[0] == True:
            consecutive_price_decrease = False
            for x in range(NUMBER_OF_DAYS - 1):
                if trend[x + 1] != True:
                    consecutive_price_increase = False
                    break

        elif trend[0] == False:
            consecutive_price_increase = False
            for x in range(NUMBER_OF_DAYS - 1):
                if trend[x + 1] != False:
                    consecutive_price_increase = False
                    break
        else:
            consecutive_price_increase = False
            consecutive_price_decrease = False

        if consecutive_price_increase:
            currentPos[stock_number] += 1
        elif consecutive_price_decrease:
            currentPos[stock_number] -= 1

    return currentPos

    
