import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['figure.dpi'] = 150
# pd.options.display.max_rows = 20

# prices_data = pd.read_csv("prices.txt", nrows = 5, delim_whitespace = True, header = None)
prices_data = pd.read_csv("prices.txt", delim_whitespace = True, header = None)
# prices_data[0].plot()
# prices_data[55].plot()
prices_data.plot()

plt.show()

list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(list[2][2])


nInst = 100
currentPos = np.zeros(nInst) # array of 100 zeros

# def getMyPosition (prcSoFar):
#     global currentPos

#     # Build your function body here
    
#     # current_day = np.shape(prcSoFar)[0]
#     print(prcSoFar)
#     # print("CURRENT DAY", current_day)

#     return currentPos


NUMBER_OF_DAYS = 3

def getMyPosition (prcSoFar):
    global currentPos

    # Build your function body here

    current_day = np.shape(prcSoFar)[1]

    for i in range(nInst):
        trend = []
        stock_number = i

        #       if True, price increased, if False, price decreased
        if (current_day > NUMBER_OF_DAYS):
            for x in range(NUMBER_OF_DAYS):
                if prcSoFar[stock_number - 1, current_day - x] - prcSoFar[stock_number - 1, current_day - x - 1] > 0:
                    trend.append(True)
                elif prcSoFar[stock_number - 1, current_day - x] - prcSoFar[stock_number - 1, current_day - x - 1] < 0:
                    trend.append(False)
                else:
                    trend.append(None)

        print("TREND", trend)

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