import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['figure.dpi'] = 150

# prices_data = pd.read_csv("prices.txt", delim_whitespace = True, header = None)
# prices_data.plot()
# plt.show()

nInst=100
# nInst=3
currentPos = np.zeros(nInst)
init_stock_price = np.zeros(nInst)


def getMyPosition(prcSoFar): # called ONCE every DAY
    global currentPos

    # Build your function body here
    # print("PRCSOFAR", prcSoFar)
    # print(prcSoFar[1, 0])

    current_day = np.shape(prcSoFar)[1] - 1
    # print("CURRENT_DAY", current_day)

    # Create an average of all the stocks
    # More sophesiticated model would group the stocks based on the correlation
    if current_day == 1:
        for i in range(nInst):
            init_stock_price[i] = prcSoFar[i, 0]

    stock_days = len(prcSoFar[0])

    # PUT THE PRICE RATIO IN A DICTIONARY. key:value = [stock, stock]:[PR1, PR2, PR3 ...]
    price_ratio_dict = {}

    # DETERMINE THE PRICE RATIO BETWEEN A STOCK AND EVERY OTHER
    for i in range(stock_days):
        if i < stock_days:
            for x in range(len(prcSoFar)):
                for y in range(x+1, len(prcSoFar)):
                    ratio = prcSoFar[x][i] / prcSoFar[y][i]
                    # print([x, y], ratio)

                    if (x, y) in price_ratio_dict:
                        price_ratio_dict[(x, y)].append(ratio)
                    else:
                        price_ratio_dict[(x, y)] = [ratio]

    # print("DICT", price_ratio_dict)
    # print(price_ratio_dict[(0,1)])
    # print("STDEV", np.std(price_ratio_dict[(0,1)]))

    # print("MEAN", np.mean(price_ratio_dict[(0,1)]))
    # print(price_ratio_dict[(0,1)])
    price_ratio_std_mean_dict = {}

    for stock_pair in price_ratio_dict: # will store in dictionary (stock pair):[stdev of PRs, mean of PRs]
        price_ratio_std_mean_dict[stock_pair] = [np.std(price_ratio_dict[stock_pair]), np.mean(price_ratio_dict[stock_pair])]

    # print("PRICE RATIO STDEV DICT", price_ratio_std_mean_dict)







    index_sum = 0
    for i in range(nInst):
        index_sum += prcSoFar[i, current_day] / init_stock_price[i]

    index = index_sum / 100

    # If the stock is more expensive than the average, buy, else, sell
    prc_gap = index_sum * 0.1
    for i in range(nInst):
        max_trade = np.floor(10000 / prcSoFar[i, current_day])
        if (prcSoFar[i, current_day] / init_stock_price[i]) > index - prc_gap:
            currentPos[i] = - max_trade
        elif (prcSoFar[i, current_day] / init_stock_price[i]) < index + prc_gap:
            currentPos[i] = max_trade

        if (prcSoFar[i, current_day] / init_stock_price[i]) == index:
            currentPos[i] = 0

    return currentPos





def createHashMap():
    pass




# arr = [40.44, 4.90, 30.92, 0.58, 4.88]

# for i in range(len(arr)):
#     if i < len(arr) - 1:
#         for x in range(i+1,len(arr)):
#             ratio = arr[i] / arr[x]
#             print(ratio)

# arr = [[40.44,4.90,30.92,0.58,4.88],[30.44,3.90,20.92,0.058,3.88]]

# for i in range(5):
#     if i < 5:
#         for x in range(len(arr)):
#             for y in range(x+1, len(arr)):
#                 ratio = arr[x][i] / arr[y][i]
#                 print(ratio)

# arr = [20, 2, 7, 1, 34]

# print(np.std(arr))
