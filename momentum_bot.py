# add a way to make it so its not constantly the same 102 stocks being bought/sold?

import time
import threading
import pickle
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas_market_calendars as pmc
import yfinance as yf
from ADX import DMI
from stock_class_adx import Stock


def stopLoss(stock):
    yfdata = yf.Ticker(stock.symbol)
    bought_days_ago = (float(time.time()) - float(stock.last_bought_time))/60/60/24
    data = yfdata.history(period=f'{int(bought_days_ago)}d', interval='1d') # +1 ?
    high = data['High']
    highs = high.values.tolist()
    highs.reverse() # current -> past
    highs = highs[0:int(bought_days_ago)]
    max_list = max(highs)
    currentprice = data['Close'][-1]
    if (((max_list - currentprice) / max_list) * 100) >= 5:
        return 'SELL'

def didIntersection(DIs, days):
    postops = 0
    for i in DIs[0:days]:
        if i[0] > i[1]:
            postops += 1
    if postops == 0 or postops == days:
        return False
    else:
        return True

def getintersections(DIs, days):
    intersections = 0
    posneglist = []
    pos = [i[0] for i in DIs]
    neg = [i[1] for i in DIs]

    for i in range(days):
        if pos[i] > neg[i]:
            posneglist.append('pos')
        else:
            posneglist.append('neg')
    for i in range(len(posneglist)):
        try:
            if posneglist[i] != posneglist[i+1]:
                intersections += 1
        except IndexError as e:
            pass
    return intersections

def inwarding(DIs):
    diff_list = []
    for i in DIs[0:2]:
        diff_list.append(abs(i[0] - i[1]))
    if diff_list[1] > diff_list[0]:
        return True # it is going inward
    else:
        return False # it is going outward or parallel

def isTradingHours():
    NASDAQ = pmc.get_calendar('NASDAQ')
    timezone = NASDAQ.tz.zone

    holidays = NASDAQ.holidays()
    dum = holidays.holidays

    holidays = []
    for i in dum:
        holidays.append(str(i))

    full_date = str(datetime.today())
    reduced_date = full_date.split(' ')
    h_m_s = reduced_date[1]
    dum_time = h_m_s.split(':')
    hour = dum_time[0]
    minute = dum_time[1]
    time = float(str(hour) + '.' + str(minute))
    weekday = datetime.today().weekday()

    today = str(datetime.today()).split(' ')
    today = today[0]

    if time > 9.32 and time < 15.58 and weekday != 5 and weekday != 6 and today not in holidays: # original 9.3, 16
        return True
    else:
        return False

def getPrice(stock):
    url = f'https://finance.yahoo.com/quote/{stock}/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    stock_price = soup.select_one('span[class^="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"]').contents[0]
    stock_price = stock_price.replace(',', '')
    return float(stock_price)

def main(stock):
    global errors
    try:
        DIs = DMI(stock.symbol)
        pos_DI = [i[0] for i in DIs]
        neg_DI = [i[1] for i in DIs]
        price = getPrice(stock.symbol)
    except:
        errors.append('Server Connection Error') # <- Probably
        quit()
    close_req = 0.4 # maybe edit (0.3?) # original 0.5

    if (abs(pos_DI[0] - neg_DI[0]) <= close_req and pos_DI[0] > neg_DI[0] and didIntersection(DIs, 5) == False and stock.holding > 0 and inwarding(DIs)) or (getintersections(DIs, 5) >= 2 and stock.holding > 0) or (stock.holding > 0 and (time.time() - stock.last_bought) < 86400 and didIntersection(DIs, 3) == False and inwarding(DIs) == False) or (stopLoss(stock) == 'SELL' and stock.holding > 0 and (time.time() - stock.last_bought) > 86400):
        print(f'{stock.symbol}: SOLD')
        stock.holding = 0
        stock.bought_for_amt = 0
        stock.last_bought_time = 0
        stock.last_sold_time = time.time()
        stock.eversold += price

    elif abs(pos_DI[0] - neg_DI[0]) <= close_req and neg_DI[0] > pos_DI[0] and didIntersection(DIs, 5) == False and (time.time() - stock.last_bought) > 86400 and inwarding(DIs) and stock.holding == 0:
        print(f'{stock.symbol}: BOUGHT')
        stock.holding += 1
        stock.last_sold_time = 0
        stock.last_bought_time = time.time()
        stock.bought_for_amt += price
        stock.everbought += price

    else:
        # print(f'{stock.symbol}: WAIT')
        pass

while True: # THE main loop
    if isTradingHours():
        with open('adx_stocklist.pkl', 'rb') as f:
            stocks = pickle.load(f)

        threadlist = []
        errors = []
        for i in stocks:
            dothread = threading.Thread(target=main, args=(i,))
            threadlist.append(dothread)
            dothread.start()
        for i in threadlist:
            i.join()

        try:
            print(errors[0])
        except:
            pass

        with open('adx_stocklist.pkl', 'wb') as f:
            pickle.dump(stocks, f)

        print('Finished a loop... ' + datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S").strftime("%r"))
        time.sleep(60) # or however long you want to wait in between getting new data / checking whether to buy/sell.
    else:
        print('It is not Trading hours... ' + datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S").strftime("%r"))
        time.sleep(300)
