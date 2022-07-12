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
NO_OF_DAYS = 10

average_volatility = np.zeros(nInst)
VOL_NO_OF_DAYS = 10

max_price = np.zeros(nInst)
min_price = np.zeros(nInst)

# moving_average = np.zeros(nInst)
# for i in range(nInst):
#     moving_average[i] = []


def getMyPosition(prcSoFar):
    global currentPos
    # Build your function body here
    current_day = np.shape(prcSoFar)[1] - 1

    # # Price filter
    # for stock in range(nInst):
    #     if current_day + 1 > VOL_NO_OF_DAYS:
    #         for x in range(VOL_NO_OF_DAYS):
    #             average_volatility[stock] += np.absolute((prcSoFar[stock, current_day - x] - prcSoFar[stock, current_day - x - 1]) / prcSoFar[stock, current_day - x - 1])
    #         average_volatility[stock] = average_volatility[stock] / VOL_NO_OF_DAYS
    # sorted_index_array = np.argsort(average_volatility)
    # sorted_avg_vol = average_volatility[sorted_index_array]
    # print(sorted_avg_vol[int(99 - 100/10)])
    #
    # # Max/Min price
    # for i in range(nInst):
    #     # init min/max price
    #     if current_day == 0:
    #         min_price[i] = prcSoFar[i, 0]
    #         max_price[i] = prcSoFar[i, 0]

    # # Moving average
    # MA_NUMBER = 5
    # if current_day + 1 > MA_NUMBER:
    #     for i in range(nInst):
    #         stock_price_sum = 0
    #         for x in range(MA_NUMBER):
    #             stock_price_sum += prcSoFar[i, current_day - x]
    #         avg_stock_price[i] = stock_price_sum / MA_NUMBER
    # else:
    #     col = np.zeros(nInst)
    #     for i in range(nInst):
    #         col[i] = []
    #     for i in range(nInst):
    #         pass

    # Correlating stocks
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

        print(correlation_dictionary)


    # for i in range(nInst):
    #     if current_day > NO_OF_DAYS:
    #         if average_volatility[i] >= sorted_avg_vol[99]:
    #             max_trade = np.floor(10000 / prcSoFar[i, current_day - 1])
    #             if prcSoFar[i, current_day - VOL_NO_OF_DAYS] > prcSoFar[i, current_day]:
    #                 currentPos[i] = -max_trade
    #             if prcSoFar[i, current_day - VOL_NO_OF_DAYS] < prcSoFar[i, current_day]:
    #                 currentPos[i] = max_trade
    #
    #
    # for i in range(nInst):
    #     trend = []
    #     stock_number = i
    #
    #     #       if True, price increased, if False, price decreased
    #     if (current_day + 1 > NO_OF_DAYS):
    #         for x in range(NO_OF_DAYS):
    #             price_difference = prcSoFar[stock_number, current_day - x] - prcSoFar[stock_number, current_day - x - 1]
    #             if price_difference > 0:
    #                 trend.append(True)
    #             elif price_difference < 0:
    #                 trend.append(False)
    #             else:
    #                 trend.append(None)
    #
    #         consecutive_price_increase = True
    #         consecutive_price_decrease = True
    #
    #         if trend[0] == True:
    #             consecutive_price_decrease = False
    #             for x in range(NO_OF_DAYS - 1):
    #                 if trend[x + 1] != True:
    #                     consecutive_price_increase = False
    #                     break
    #
    #         elif trend[0] == False:
    #             consecutive_price_increase = False
    #             for x in range(NO_OF_DAYS - 1):
    #                 if trend[x + 1] != False:
    #                     consecutive_price_increase = False
    #                     break
    #         else:
    #             consecutive_price_increase = False
    #             consecutive_price_decrease = False

    return currentPos
