import yfinance as yf
import time

class Stock:
    def __init__(self, symbol, last_bought_time=0, last_sold_time = 0, holding=0, bought_for_amt=0, everbought=0, eversold=0):
        self.symbol = symbol
        self.last_bought_time = last_bought_time
        self.last_sold_time = last_sold_time
        self.holding = holding
        self.bought_for_amt = bought_for_amt
        self.everbought = everbought
        self.eversold = eversold

    def reset(self):
        self.last_bought_time = 0
        self.last_sold_time = 0
        self.holding = 0
        self.bought_for_amt = 0
        self.everbought = 0
        self.eversold = 0

    def buy(self):
        price = yf.Ticker(self.symbol).info['regularMarketPrice'] # price
        self.holding += 1
        self.last_sold_time = 0
        self.last_bought_time = time.time()
        self.bought_for_amt += price
        self.everbought += price

    def sell(self):
        self.holding = 0
        self.bought_for_amt = 0
        self.last_bought_time = 0
        self.last_sold_time = time.time()
        self.eversold += yf.Ticker(self.symbol).info['regularMarketPrice']

    def getPrice(self):
        return yf.Ticker(self.symbol).info['regularMarketPrice']

    def getTotalProfit(self, price=False): # unrealized + realized
        eversold = self.eversold
        if not price:
            price = yf.Ticker(self.symbol).info['regularMarketPrice']
        if self.holding > 0:
            eversold += (self.holding*price) # price
            total_profit = eversold - self.everbought
            total_profit_perc = total_profit / eversold
        else:
            total_profit = 0
            total_profit_perc = 0
        return total_profit, total_profit_perc

    def getDailyProfit(self):
        data = yf.Ticker(self.symbol).history(period='2d', interval='1d')
        if self.holding > 0 and (time.time() - self.last_bought_time) >= 86400:
            # if holding > 1 day and holding, profit = current price - yesterdays close, elif we bought today, profit = current price - bought for amt
            daily_profit = data['Close'][1] - data['Close'][0]
            daily_profit_perc = daily_profit / data['Close'][1]
            previous_close = data['Close'][1]
        elif self.holding > 0 and (time.time() - self.last_bought_time) < 86400:
            daily_profit = data['Close'][1] - self.bought_for_amt
            daily_profit_perc = daily_profit / data['Close'][1]
        else:
            daily_profit = 0
            daily_profit_perc = 0
            previous_close = 0
        return daily_profit, daily_profit_perc

    def getHoldingTime(self):
        if self.last_bought_time != 0:
            return (time.time() - self.last_bought_time)/60/60/24
        else:
            return 0

    def getSimulatedEversold(self, price=False):
        eversold = self.eversold
        if not price:
            price = yf.Ticker(self.symbol).info['regularMarketPrice']
        eversold += (self.holding*price)
        return eversold

    def getEverProfit(self, price=False):
        if not price:
            price = yf.Ticker(self.symbol).info['regularMarketPrice']

        if self.holding > 0 and self.eversold != 0:
            ever_profit = (self.eversold - (self.everbought - self.bought_for_amt)) + (price - self.bought_for_amt)
        elif self.holding > 0 and self.eversold == 0:
            ever_profit = price - self.bought_for_amt
        else:
            ever_profit = self.eversold - self.everbought

        return ever_profit
