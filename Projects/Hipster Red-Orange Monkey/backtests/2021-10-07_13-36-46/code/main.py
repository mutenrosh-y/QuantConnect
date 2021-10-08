from collections import deque
from AlgorithmImports import *
class HipsterRedOrangeMonkey(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2021,8,4)
        self.SetCash(100000)
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol

        self.sma = self.SMA(self.spy, 30, Resolution.Daily)

        #Feed SMA indicator with Historical Data
        #closing_prices = self.History(self.spy, 30, Resolution.Daily)["close"]
        #for time, price in closing_prices.loc[self.spy].items():
        #    self.sma.Update(time, price)

        self.sma = CustomSMA("CustomSMA", 30)
        self.RegisterIndicator(self.spy, self.sma, Resolution.Daily)


    def OnData(self, data):
        if not self.sma.IsReady:
            return

        hist = self.History(self.spy, timedelta(365), Resolution.Daily)
        low = min(hist["low"])
        high = max( hist["high"])

        price = self.Securities[self.spy].Price

        #if price * 0.95 >= high and self.sma.Current.Value < price:
        if price * 1.05 >= high and self.sma.Current.Value < price:
            if not self.Portfolio[self.spy].IsLong:
                self.SetHoldings(self.spy, 1)

        #if price * 1.05 <= low and self.sma.Current.Value > price:
        elif price * 0.95 <= low and self.sma.Current.Value > price:
            if not self.Portfolio[self.spy].IsShort:
                self.SetHoldings(self.spy, -1)

        else:
            self.Liquidate()

        self.Plot("BenchMark", "52w-High", high)
        self.Plot("BenchMark", "52w-Low", low)
        self.Plot("BenchMark", "SMA", self.sma.Current.Value)

class CustomSMA(PythonIndicator):

    def __init__(self, name, period):
        self.Name = name
        self.Time = datetime.min
        self.Value = 0
        self.queue = deque(maxlen=period)

    def Update(self, input):
        self.queue.appendleft(input.Close)
        self.Time = input.EndTime
        count = len(self.queue)
        self.Value = sum(self.queue)/count
        return (count == self.queue.maxlen)
