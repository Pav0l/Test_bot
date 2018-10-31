import threading
import bitmex
import datetime
from bitmex_websocket import BitMEXWebsocket
from api_info import bitmex_testnet_api_key, bitmex_testnet_api_secret

currency_pair = "XBTUSD"
count = 10
interval = "1m" # Available options:[1m,5m,1h,1d]

ws = BitMEXWebsocket(endpoint="https://testnet.bitmex.com/api/v1", symbol=currency_pair, api_key=bitmex_testnet_api_key,
                     api_secret=bitmex_testnet_api_secret)
client = bitmex.bitmex(test=True, api_key=bitmex_testnet_api_key,
                       api_secret=bitmex_testnet_api_secret)

def slowLoop():
    tradeData = client.Trade.Trade_getBucketed(symbol=currency_pair, binSize=interval,
                                           count=count, reverse=True).result()
    print(str(datetime.datetime.now().replace(microsecond=0)) + "; Bitmex_Trade_getBucketed: " + str(tradeData))
    threading.Timer(60, slowLoop).start()

def fastLoop():
  # get_ticker() depends on tickLog being set in the dict. This occurs when getInstrument() is called.
  # As a workaround you can call ws.get_instrument() every time you are calling get_ticker()
    ws.get_instrument()
    ticker_price = ws.get_ticker().get("last")
    print(str(datetime.datetime.now().replace(microsecond=0)) + "; Ticker price: " + str(ticker_price))
    threading.Timer(10, fastLoop).start()

if __name__ == "__main__":
    threading.Thread(target=slowLoop()).start()
    threading.Thread(target=fastLoop()).start()
