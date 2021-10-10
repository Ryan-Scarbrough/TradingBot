# from stock_class import Stock
from stock_class_adx import Stock
import pickle

with open('adx_stocklist.pkl', 'rb') as f:
    stocks = pickle.load(f)

# from stock_class_bb import Stock

def convert(stocks):
    newstocks = []
    for i in stocks:
        symbol = i.symbol
        last_bought_time = i.last_bought_time
        last_sold_time = i.last_sold_time
        holding = i.holding
        bought_for_amt = i.bought_for_amt
        everbought = i.everbought
        eversold = i.eversold
        newObj = Stock(symbol, last_bought_time, last_sold_time, holding, bought_for_amt, everbought, eversold)
        newstocks.append(newObj)
    return newstocks

def create(tickers):
    newstocks = []
    for i in tickers:
        symbol = i
        last_bought_time = 0
        last_sold_time = 0
        holding = 0
        bought_for_amt = 0
        everbought = 0
        eversold = 0
        newObj = Stock(symbol, last_bought_time, last_sold_time, holding, bought_for_amt, everbought, eversold)
        newstocks.append(newObj)
    return newstocks

# tickers = ['AAPL', 'ADBE', 'ADI', 'ADP', 'ADSK', 'AEP', 'ALGN', 'ALXN', 'AMAT', 'AMD', 'AMGN', 'AMZN', 'ANSS', 'ASML', 'ATVI', 'AVGO', 'BIDU', 'BIIB', 'BKNG', 'CDNS', 'CDW', 'CERN', 'CHKP', 'CHTR', 'CMCSA', 'COST', 'CPRT', 'CSCO', 'CSX', 'CTAS', 'CTSH', 'DLTR', 'DOCU', 'DXCM', 'EA', 'EBAY', 'EXC', 'FAST', 'FB', 'FISV', 'FOX', 'FOXA', 'GILD', 'GOOG', 'GOOGL', 'IDXX', 'ILMN', 'INCY', 'INTC', 'INTU', 'ISRG', 'JD', 'KDP', 'KHC', 'KLAC', 'LRCX', 'LULU', 'MAR', 'MCHP', 'MDLZ', 'MELI', 'MNST', 'MRNA', 'MRVL', 'MSFT', 'MTCH', 'MU', 'MXIM', 'NFLX', 'NTES', 'NVDA', 'NXPI', 'OKTA', 'ORLY', 'PAYX', 'PCAR', 'PDD', 'PEP', 'PTON', 'PYPL', 'QCOM', 'REGN', 'ROST', 'SBUX', 'SGEN', 'SIRI', 'SNPS', 'SPLK', 'SWKS', 'TCOM', 'TEAM', 'TMUS', 'TSLA', 'TXN', 'VRSK', 'VRSN', 'VRTX', 'WBA', 'WDAY', 'XEL', 'XLNX', 'ZM']

newstocks = convert(stocks)

with open('adx_stocklist.pkl', 'wb') as f:
    pickle.dump(newstocks, f)
