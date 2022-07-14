import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['figure.dpi'] = 150

prices_data = pd.read_csv("prices.txt", delim_whitespace = True, header = None)
prices_data[79].plot()
prices_data[2].plot()
plt.show()

nInst=100
# nInst=3
currentPos = np.zeros(nInst)
init_stock_price = np.zeros(nInst)


def getMyPosition(prcSoFar): # called ONCE every DAY
    global currentPos

    # for x in range(len(prcSoFar)):
        # print(x, prcSoFar[x][-1])

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

    ########################################################################################
    ### UTILISE THE CORRELATION_DICTIONARY
    N_DAYS = 4
    correlation_vector = np.arange(100 * N_DAYS).reshape(100, N_DAYS)
    PERCENTAGE_THRESHOLD = 0.001
    if current_day > N_DAYS:
        correlation_dictionary = {}
        for i in range(nInst):
            for j in range(N_DAYS):
                if (prcSoFar[i, current_day - j] - prcSoFar[i, current_day - j - 1]) / prcSoFar[i, current_day - j - 1] > PERCENTAGE_THRESHOLD:
                    correlation_vector[i, N_DAYS - 1 - j] = 1
                elif (prcSoFar[i, current_day - j] - prcSoFar[i, current_day - j - 1]) / prcSoFar[i, current_day - j - 1] < -PERCENTAGE_THRESHOLD:
                    correlation_vector[i, N_DAYS - 1 - j] = -1
                else:
                    correlation_vector[i, N_DAYS - 1 - j] = 0

        for i in range(nInst):
            if tuple(correlation_vector[i]) not in correlation_dictionary:
                correlation_dictionary[tuple(correlation_vector[i])] = [i]
            else:
                correlation_dictionary[tuple(correlation_vector[i])].append(i)

        # data cleaning
        # remove stocks for which we have found a pattern but no correlation partner
        to_remove = []
        for pattern in correlation_dictionary:
            if len(correlation_dictionary[pattern]) == 1:
                to_remove.append(pattern)
                # print(to_remove)

        for i in to_remove:
            del correlation_dictionary[i]

        # print(correlation_dictionary)

    ########################################################################################

    # pick two of the closest stock in terms of price for each key:value in correlation_dictionary

        stock_prices_ls = []
        # PUT THE PRICE RATIO IN A DICTIONARY. key:value = [stock, stock]:[PR1, PR2, PR3 ...]
        # MOVED HERE
        price_ratio_dict = {}

        for stock_pattern in correlation_dictionary: # stock_pattern = (-1, 0, -1, -1)
            similar_stock = correlation_dictionary[stock_pattern] # similar_stock = [2, 12, 68]
            highest_subset_stock_prices_ls = []
            ligma_nuts = {}
            if len(similar_stock) > 2:
                for stock in similar_stock: # stock = 2, 12, 68
                    # GET THE HIGHEST TWO STOCKS
                    ligma_nuts[stock] = prcSoFar[stock, -1] # {2:4.90, 12:34.87, ...}
                # stocks_descending = sorted(ligma_nuts.values(), reverse=True) # [54.89, 27.49, 15.55]
                # print("LIGMA", stocks_descending[0].keys())
                sorted_stock_group = sorted(ligma_nuts.items(), key=lambda x: x[1], reverse=True) # [(2, 30.71), (12, 27.25), (68, 18.08)]
                # stock_pair = sorted_stock_group[0:2]
                # print(stock_pair)
                container = []
                for stock_and_price in sorted_stock_group[0:2]:
                    container.append(stock_and_price[0])
                # print("CONTAINER", container)
                price_ratio_dict[tuple(container)] = []

            else:
                # print("SIMSTOCK", similar_stock)
                price_ratio_dict[tuple(similar_stock)] = []
            # append(similar_stock)

        # print(price_ratio_dict)

        # print(stock_prices_ls)

        # for stock_correlation_group in stock_prices_ls:
        #     if len(stock_correlation_group) > 2:
        #         stock_correlation_group.sort(reverse = True)
        # print(stock_prices_ls)


        # # PUT THE PRICE RATIO IN A DICTIONARY. key:value = [stock, stock]:[PR1, PR2, PR3 ...]
        # MOVED UP
        # price_ratio_dict = {}

        # DETERMINE THE PRICE RATIO BETWEEN A STOCK AND EVERY OTHER
        # for i in range(stock_days):
        #     if i < stock_days:
        #         for x in range(len(prcSoFar)):
        #         # for x in range(price_ratio_dict.keys()):
        #             for y in range(x+1, len(prcSoFar)):
        #                 ratio = prcSoFar[x][i] / prcSoFar[y][i]
        #                 # print([x, y], ratio)

        #                 if (x, y) in price_ratio_dict:
        #                     price_ratio_dict[(x, y)].append(ratio)
        #                 else:
        #                     price_ratio_dict[(x, y)] = [ratio]

        """price_ratio_dict = {(stock, pair) : [today's price ratio, historical price ratio mean, price ratio standard deviation]}"""

        for pair in price_ratio_dict: # (79, 2), (4, 68), ...

            today_pr = prcSoFar[pair[0], -1] / prcSoFar[pair[1], -1]

            historical_pr = []
            for day in range(stock_days):
                historical_pr.append(prcSoFar[pair[0], day] / prcSoFar[pair[1], day])

            pair_historical_pr_mean = np.mean(historical_pr)
            pair_historical_pr_stdev = np.std(historical_pr)

            price_ratio_dict[pair] = [today_pr, pair_historical_pr_mean, pair_historical_pr_stdev]
        # print("ABCD", price_ratio_dict)          


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

            PR_latest = price_ratio_dict[pair][0]
            PR_mean = price_ratio_dict[pair][1]
            PR_std = price_ratio_dict[pair][2]

            PR_stdev_1 = PR_mean + PR_std
            PR_stdev_2 = PR_stdev_1 + PR_std
            PR_stdev_1neg = PR_mean - PR_std
            PR_stdev_2neg = PR_stdev_1neg - PR_std

            
            numerator_stock = pair[0]
            denominator_stock = pair[1]


            todays_prc_numerator = prcSoFar[numerator_stock][-1]
            todays_prc_denominator = prcSoFar[denominator_stock][-1]

            if current_day >= 1:
                yesterdays_prc_numerator = prcSoFar[numerator_stock][-2]
                yesterdays_prc_denominator = prcSoFar[denominator_stock][-2]

                percentage_change_numerator = todays_prc_numerator / yesterdays_prc_numerator
                percentage_change_denominator = todays_prc_denominator / yesterdays_prc_denominator

                """ first determine who the under/over-performers are"""

                if percentage_change_numerator > percentage_change_denominator:
                    underperformer = denominator_stock
                    overperformer = numerator_stock

                else:
                    overperformer = denominator_stock
                    underperformer = numerator_stock

            else:
                return currentPos

            if PR_latest == PR_mean:
                pass

            elif PR_latest > PR_mean and PR_stdev_1 > PR_latest:
            #     # sell X of the overperformer
            #     # buy X of the underperformer
                currentPos[overperformer] -= 5
                currentPos[underperformer] += 5
                

            elif PR_latest > PR_stdev_1 and PR_stdev_2 > PR_latest:
                # sell XX of the overperformer
                # buy XX of the underperformer
                currentPos[overperformer] -= 10
                currentPos[underperformer] += 10

                # ACCESS PREV DAYS DATA TO DETERMINE PERCENTAGE PRICE CHANGES

            elif PR_latest > PR_stdev_2:
                # sell XXX of the overperformer
                # buy XXX of the underperformer
                currentPos[overperformer] -= 20
                currentPos[underperformer] += 20

            elif PR_latest < PR_mean and PR_stdev_1neg < PR_latest:
                # buy X of the overperformer
                # sell X of the underperformer
                currentPos[overperformer] += 5
                currentPos[underperformer] -= 5
                
            
            elif PR_latest < PR_stdev_1neg and PR_stdev_2neg < PR_latest:
                # buy XX of the overperformer
                # sell XX of the underperformer
                currentPos[overperformer] += 10
                currentPos[underperformer] -= 10

            else:
                # buy XXX of the overperformer
                # sell XXX of the underperformer
                currentPos[overperformer] += 20
                currentPos[underperformer] -= 20


        """ THRESHOLD INDEX ALGORITHM """

        # index_sum = 0
        # for i in range(nInst):
        #     index_sum += prcSoFar[i, current_day] / init_stock_price[i]

        # index = index_sum / 100

        # # If the stock is more expensive than the average, buy, else, sell
        # prc_gap = index_sum * 0.1
        # for i in range(nInst):
        #     max_trade = np.floor(10000 / prcSoFar[i, current_day])
        #     if (prcSoFar[i, current_day] / init_stock_price[i]) > index - prc_gap:
        #         currentPos[i] = - max_trade
        #     elif (prcSoFar[i, current_day] / init_stock_price[i]) < index + prc_gap:
        #         currentPos[i] = max_trade

        #     if (prcSoFar[i, current_day] / init_stock_price[i]) == index:
        #         currentPos[i] = 0

    return currentPos

    # else:
    #     return currentPos


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
