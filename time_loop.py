# THIS IS A TIME LOOP TO REQUEST TIME AND PRICE DATA FOR SPECIFIED CURRENCY PAIR FROM COINBASE.
import time
import sys
from coinbase.wallet.client import Client
from api_info import cb_api_secret, cb_api_key

# Pulling data from COINBASE = currency pair, price, time
client = Client(cb_api_key, cb_api_secret)
currency_pair = "BTC-USD"

def main(argv):
    period = 30
    while True:
        cb_buy_price = client.get_buy_price(currency_pair=currency_pair).get("amount")
        cb_sell_price = client.get_sell_price(currency_pair=currency_pair).get("amount")
        cb_spot_price = client.get_spot_price(currency_pair=currency_pair).get("amount")
        cb_time = client.get_time().get("iso")
        print(cb_time + "; Currency pair: " + currency_pair + "; BUY price: " + cb_buy_price + "; SELL price: "
              + cb_sell_price + "; SPOT price: " + cb_spot_price)
        time.sleep(period)

if __name__ == "__main__":
    main(sys.argv[1:])
