import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['figure.dpi'] = 150

# prices_data = pd.read_csv("prices.txt", delim_whitespace = True, header = None)
# prices_data.plot()
# plt.show()

# nInst=100
nInst=3
currentPos = np.zeros(nInst)
init_stock_price = np.zeros(nInst)


def getMyPosition(prcSoFar): # called ONCE every DAY
    global currentPos

    for x in range(len(prcSoFar)):
        print(x, prcSoFar[x][-1])

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

    # plt.rcParams["figure.figsize"] = [7.50, 3.50]
    # plt.rcParams["figure.autolayout"] = True

    # # y = np.price_ratio_dict[(0, 2)]
    # # x = np.sort(y)

    # plt.title = "Stock pair price ratios"
    # plt.plot(price_ratio_dict[(0, 2)], color = "blue")

    # plt.show()

    """ PSEUDOCODE 
    
    Get today's price ratio
    
    1. PR is above the mean but below +STDEV:
        sell X of the overperformer
        buy X of the underperformer

    2. PR is above +STDEV but below ++STDEV:
        sell XX of the overperformer
        buy XX of the underperformer

    3. PR is above ++STDEV:
        sell XXX of the overperformer
        buy XXX of the underperformer
    
    """

    # for i in range(stock_days):
    #     if i < stock_days:
    #         for x in range(len(prcSoFar)):

    for pair in price_ratio_dict:

        PR_mean = price_ratio_std_mean_dict[pair][1]

        PR_stdev_1 = PR_mean + price_ratio_std_mean_dict[pair][0]
        PR_stdev_2 = PR_stdev_1 + price_ratio_std_mean_dict[pair][0]
        PR_stdev_1a = PR_mean - price_ratio_std_mean_dict[pair][0]
        PR_stdev_2a = PR_stdev_1 - price_ratio_std_mean_dict[pair][0]

        latest_pr = pair, price_ratio_dict[pair][-1]
        # should print the latest day's price ratio

        if latest_pr == PR_mean:
            pass

        elif latest_pr > PR_mean and PR_stdev_1 > latest_pr:
            # sell X of the overperformer
            # buy X of the underperformer

            """ first determine who the under/over-performers are"""
            

            pass

        elif latest_pr > PR_stdev_1 and PR_stdev_2 > latest_pr:
            # sell XX of the overperformer
            # buy XX of the underperformer
            pass

        elif latest_pr > PR_stdev_2:
            # sell XXX of the overperformer
            # buy XXX of the underperformer
            pass

        elif latest_pr < PR_mean and PR_stdev_1a < latest_pr:
            # buy X of the overperformer
            # sell X of the underperformer
            pass
        
        elif latest_pr < PR_stdev_1a and PR_stdev_2a < latest_pr:
            # buy XX of the overperformer
            # sell XX of the underperformer
            pass

        else:
            # buy XXX of the overperformer
            # sell XXX of the underperformer
            pass



    #  Compare today's PR with above measures














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
