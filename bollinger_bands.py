import statistics
import yfinance as yf

def BB(stock):
    ticker = yf.Ticker(str(stock))
    data = ticker.history(period='120d', interval='1d')
    high = data['High'].values.tolist()
    low = data['Low'].values.tolist()
    close = data['Close'].values.tolist()


    TP_list = [] # past -> current
    for i in range(len(high)):
        TP = (high[i] + low[i] + close[i])/3 #typical price
        TP_list.append(TP)
    BOLUs = []
    BOLLs = []
    MA20 = []
    for i in range(100):
        MA_TP = sum(TP_list[i:i+20])/20
        BOLU = MA_TP+(2*statistics.stdev(TP_list[i:i+20]))
        BOLL = MA_TP-(2*statistics.stdev(TP_list[i:i+20]))
        BOLUs.append(BOLU)
        BOLLs.append(BOLL)
        MA20.append(MA_TP)

    return BOLUs, BOLLs, MA20

# data = calcBollingerBands('AAPL')
