from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import time

from datetime import datetime

import pytz

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def historicalData(self, reqId, bar):
        print("HistoricalData. ", reqId, " Date:", bar.date, "Open:", bar.open, "High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume, "Count:", bar.barCount, "WAP:", bar.wap)
        # time_paper = datetime.now(pytz.timezone('US/Central'))
        # time_paper = time.ctime(bar.date)
        # time_format = time.strftime("Day: %a, Time: %H:%M:%S, Month: %b", time.gmtime(int(bar.date)))
        time_format = time.strftime("%H:%M:%S", time.gmtime(int(bar.date)))
        print(time_format)
        print(datetime.fromtimestamp(int(bar.date)).astimezone(pytz.timezone('US/Central')).minute)

        # print(time.gmtime(int(bar.date)).(pytz.timezone('US/Central')))

def main():
    app = TestApp()

    app.connect("127.0.0.1", 7497, 1)

    # define contract for EUR.USD forex pair
    contract = Contract()

    # contract.symbol = "EUR"
    # contract.secType = "CASH"
    # contract.exchange = "IDEALPRO"
    # contract.currency = "USD"

    contract.symbol = "MES"
    contract.secType = "FUT"
    contract.exchange = "GLOBEX"
    contract.currency = "USD"
    contract.localSymbol = "MESU2"
    time.sleep(1)
    app.reqHistoricalData(1, contract, "", "40 S", "5 mins", "TRADES", 0, 2, False, [])

    app.run()
    print("END")

if __name__ == "__main__":
    main()