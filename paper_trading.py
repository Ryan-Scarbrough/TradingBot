import pickle
from stock_class_adx import Stock
import threading
import yfinance as yf
from requests.exceptions import ConnectionError

def pretty(item, param):
    if param.lower() == 'dollar':
        fixed_item = str(round(float(item), 2))
        if str(item)[0] == '-':
            new_item = '\033[91m' + '-$' + str(fixed_item)[1:] + '\033[0m'
        else:
            new_item = '\033[92m' + '+$' + str(fixed_item) + '\033[0m'
    elif param.lower() == 'percent':
        fixed_item = str(round(float(item)*100, 2))
        if str(item)[0] == '-':
            new_item = '\033[91m' + '-' + str(fixed_item)[1:] + '%' + '\033[0m'
        else:
            new_item = '\033[92m' + '+' + str(fixed_item) + '%' + '\033[0m'
    else:
        print('pretty function errored; you prob spelled something wrong dummy')
    return new_item

def getData(stock, choose_print):
    global eversold
    global daily_profit
    global ever_profit

    #TPD = Total profit dollar; TPP = total profit percent; DPD = daily profit dollar
    #DPP = Daily profit percent; E = eversold; EP = ever profit

    if stock.symbol == 'ALXN': # merged
        quit()
    try:
        price = stock.getPrice()
        while price != stock.getPrice():
            price = stock.getPrice()
        TPD = stock.getTotalProfit(price=price)[0]
        TPP = stock.getTotalProfit(price=price)[1]
        DPD = stock.getDailyProfit()[0]
        DPP = stock.getDailyProfit()[1]
        E = stock.getSimulatedEversold(price=price)
        EP = stock.getEverProfit(price=price)
    except ConnectionError:
        print(f'Connection error with {stock.symbol}')
        quit()

    eversold.append(E)
    daily_profit.append(DPD)
    ever_profit.append(EP)

    if stock.holding > 0 and choose_print:
        pretty_TPD = pretty(TPD, 'dollar')
        pretty_DPD = pretty(DPD, 'dollar')
        pretty_TPP = pretty(TPP, 'percent')
        print(f'{stock.symbol} (${price}): {pretty_TPP} | {pretty_TPD} | {stock.holding} share(s) for {round(stock.getHoldingTime(), 1)} days')

def main(choose_print=True):
    global eversold
    global daily_profit
    global ever_profit
    eversold = []
    daily_profit = []
    ever_profit = []

    with open('adx_stocklist.pkl', 'rb') as f:
        stocks = pickle.load(f)

    threadlist = []
    for stock in stocks:
        dothread = threading.Thread(target=getData, args=(stock, choose_print, ))
        threadlist.append(dothread)
        dothread.start()
    for i in threadlist:
        i.join()

    total_eversold = sum(eversold)
    daily_profit = sum(daily_profit)
    ever_profit_var = sum(ever_profit)
    total_profit_perc = (ever_profit_var/total_eversold)
    daily_profit_perc = (daily_profit/total_eversold)
    if choose_print:
        print('\n'+u'\u001b[35mToday\u001b[0m'+'\n'+f'P/L: {pretty(daily_profit, "dollar")}'+'\n'+f'Percent Change: {pretty(daily_profit_perc, "percent")}')
        print('\n'+u'\u001b[35mTotal\u001b[0m'+'\n'+f'P/L: {pretty(ever_profit_var, "dollar")}'+'\n'+f'P/L Percent: {pretty(total_profit_perc, "percent")}')
    return ever_profit_var, total_profit_perc, pretty(daily_profit, 'dollar'), pretty(daily_profit_perc, 'percent')

if __name__ == "__main__":
    main()
