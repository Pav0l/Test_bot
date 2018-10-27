# This is where you can test the algo on historic data from CB. Tests will be done on daily closing data of BTCUSD
from coinbase.wallet.client import Client
import matplotlib.pyplot as plt
from api_info import cb_api_secret, cb_api_key


client = Client(cb_api_key, cb_api_secret)
currency_pair = "BTC-USD"
period = "all"
# Entry and exit periods for trades.
entry_period = 8
exit_period = 5

# Creating a list of historical data into two lists. One with prices, one with times.
hist_data = client.get_historic_prices(currency_pair = currency_pair, period = period).get("prices")
hist_prices = []
hist_dates = []
for i in hist_data:
    hist_prices.append(float(i["price"]))
    hist_dates.append((i["time"]))
# print("Hist.prices: ", len(hist_prices), hist_prices)

# Looping through the price list and searching for values which are higher/lower than entry_period
# to specify BREAKOUT point to enter LONG/SHORT position
long_price = []
long_id = []
long_date = []
breakout_long = []
short_price = []
short_id = []
short_date = []
breakout_short = []
for a in hist_prices:
    if hist_prices.index(a) < entry_period:
        continue
    if (hist_prices.index(a)+entry_period) > hist_prices.index(hist_prices[-1]):
        break
    if a > max(hist_prices[(hist_prices.index(a)+1):(hist_prices.index(a)+entry_period)]):
        long_id.append(hist_prices.index(a))
        long_price.append(a)
        long_date.append(hist_dates[hist_prices.index(a)])
        breakout_long.append({"ID": hist_prices.index(a), "date": hist_dates[hist_prices.index(a)], "price": a })
    elif a < min(hist_prices[(hist_prices.index(a)+1):(hist_prices.index(a)+entry_period)]):
        short_id.append(hist_prices.index(a))
        short_price.append(a)
        short_date.append(hist_dates[hist_prices.index(a)])
        breakout_short.append({"ID": hist_prices.index(a), "date": hist_dates[hist_prices.index(a)], "price": a})

# Now I need to identify an exit strategy for each entry point and store the entry-exit data
exit_long = []
exit_long_price = []
for b in long_id:
    search_long_exit = hist_prices[0:(b+exit_period)]
    # print("b = ", b)
    # print("search_long_exit = ", search_long_exit)
    # for loop zacina hladat od poslednej hodnoty. takze najde posledne exity ako prve
    # a tie co mali byt ako prve budu posledne pre dany entry signal.
    # skus ci bude hladat aj pre for c in search_long_exit.reverse()
    for c in search_long_exit.__reversed__():
        # print("c =", c)
        # print("search_long_exit[c:c+5] = ", search_long_exit[(search_long_exit.index(c)):
        # (search_long_exit.index(c)+exit_period+1)])
        # print("min(search...", min(search_long_exit[(search_long_exit.index(c)):
        # (search_long_exit.index(c)+exit_period+1)]))
        # print(len(search_long_exit[(search_long_exit.index(c)):(search_long_exit.index(c)+exit_period+1)]))
        if search_long_exit.index(c) < exit_period:
            continue
        if len(search_long_exit[(search_long_exit.index(c)):(search_long_exit.index(c)+exit_period+1)]) < exit_period:
            continue
        if c <= min(search_long_exit[(search_long_exit.index(c)):(search_long_exit.index(c)+exit_period+1)]):
            exit_long_price.append(float(c))
            exit_long.append({"ID": b, "date": hist_dates[hist_prices.index(c)], "price": c})
            break
long_result = [x - y for x, y in zip(exit_long_price, long_price)]
print("LONG_results: ", sum(long_result), " USD")

exit_short = []
exit_short_price = []
for d in short_id:
    search_short_exit = hist_prices[0:(d+exit_period)]
    # print("b = ", b)
    # print("search_long_exit = ", search_long_exit)
    # for loop zacina hladat od poslednej hodnoty. takze najde posledne exity ako prve a tie co mali byt ako prve budu posledne pre dany entry signal.
    # skus ci bude hladat aj pre for c in search_long_exit.reverse()
    for e in search_short_exit.__reversed__():
        # print("c =", c)
        # print("search_long_exit[c:c+5] = ", search_long_exit[(search_long_exit.index(c)):(search_long_exit.index(c)+exit_period+1)])
        # print("min(search...", min(search_long_exit[(search_long_exit.index(c)):(search_long_exit.index(c)+exit_period+1)]))
        # print(len(search_long_exit[(search_long_exit.index(c)):(search_long_exit.index(c)+exit_period+1)]))
        if search_short_exit.index(e) < exit_period:
            continue
        if len(search_short_exit[(search_short_exit.index(e)):(search_short_exit.index(e)+exit_period+1)]) < exit_period:
            continue
        if e >= max(search_short_exit[(search_short_exit.index(e)):(search_short_exit.index(e)+exit_period+1)]):
            exit_short_price.append(float(e))
            exit_short.append({"ID": d, "date": hist_dates[hist_prices.index(e)], "price": e})
            break
short_result = [x - y for x, y in zip(short_price, exit_short_price)]
total_result = sum(short_result) + sum(long_result)
# print("SHORT_entry: ", len(short_price), short_price)
# print("SHORT_exit: ", len(exit_short_price), exit_short_price)
print("SHORT_result: ", sum(short_result), " USD")
print("TOTAL_SUM: ", total_result, " USD")
print("Start date: ", hist_dates[-1], "End date: ", hist_dates[0])

# plt.plot(hist_prices)
# plt.show()
# plt.plot(long_result)
# plt.show()
# plt.plot(short_result)
# plt.show()

