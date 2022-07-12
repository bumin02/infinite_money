import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import math

mpl.rcParams['figure.dpi'] = 150

prices_data = pd.read_csv("prices.txt", delim_whitespace=True, header=None)
prices_data.plot()
plt.show()

# prices_data

# prices_data[0].plot()
# prices_data[1].plot()

# x_values = [1, 2, 3, 4]
# y_values = [6, 5, 4, 3]
# plt.scatter(x_values, y_values)


nInst = 100
currentPos = np.zeros(nInst)
init_stock_price = np.zeros(nInst)


def getMyPosition(prcSoFar):
    global currentPos

    # Build your function body here
    # print("PRCSOFAR", prcSoFar)
    # print(prcSoFar[1, 0])

    current_day = np.shape(prcSoFar)[1] - 1
    print("CURRENT_DAY", current_day)

    # Create an average of all the stocks
    # More sophesiticated model would group the stocks based on the correlation
    if current_day == 1:
        for i in range(nInst):
            init_stock_price[i] = prcSoFar[i, 0]

    index_sum = 0
    for i in range(nInst):
        index_sum += prcSoFar[i, current_day] / init_stock_price[i]

    index = index_sum / 100

    # If the stock is more expensive than the average, buy, else, sell
    prc_gap = index_sum * 0.1
    for i in range(nInst):
        max_trade = np.floor(10000 / prcSoFar[i, current_day])
        if (prcSoFar[i, current_day] / init_stock_price[i]) > index - prc_gap:
            currentPos[i] = -max_trade
        elif (prcSoFar[i, current_day] / init_stock_price[i]) < index + prc_gap:
            currentPos[i] = max_trade

        if (prcSoFar[i, current_day] / init_stock_price[i]) == index:
            currentPos[i] = 0

    return currentPos


