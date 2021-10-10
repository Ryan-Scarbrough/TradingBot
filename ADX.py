
import yfinance as yf

def atr_wilders(data, n=14): #n = 14
    high = data['High']
    low = data['Low']
    close = data['Close']
    data['tr0'] = abs(high - low)
    data['tr1'] = abs(high - close.shift())
    data['tr2'] = abs(low - close.shift())
    tr = data[['tr0', 'tr1', 'tr2']].max(axis=1)
    atr = tr.ewm(alpha=1/n, adjust=False).mean()
    return atr[-1]

def DMI(ticker, size=5):
    yfdata = yf.Ticker(ticker)
    data = yfdata.history(period='200d', interval='1d')
    DILists = []
    for i in range(201-size, 201):
        datamod = data[0:i]
        dfdata = datamod.copy()
        datamod = datamod.values.tolist()
        datamod.reverse()
        dm_list = []
        smoothed_list = []
        for i in range(len(datamod)):
            try:
                posmov = datamod[i][1] - datamod[i+1][1]
                negmov = datamod[i+1][2] - datamod[i][2]
                if (posmov > negmov) and posmov > 0:
                    PDM = posmov
                else:
                    PDM = 0
                if (negmov > posmov) and negmov > 0:
                    NDM = negmov
                else:
                    NDM = 0
                dm_list.append([PDM, NDM])
            except:
                pass
        PDM_sum = 0
        NDM_sum = 0
        for i in dm_list[-14:-1]: # 200 ->-1, -14
            PDM_sum += i[0]
            NDM_sum += i[1]
        prior_SP = PDM_sum/14
        prior_SN = NDM_sum/14
        dm_list = dm_list[0:-14]
        dm_list.reverse()
        for i in dm_list:
            pos_smoothed = ((prior_SP*13) + i[0]) / 14
            neg_smoothed = ((prior_SN*13) + i[1]) / 14
            prior_SP = pos_smoothed
            prior_SN = neg_smoothed
            smoothed_list.append([pos_smoothed, neg_smoothed])
        smoothed_list.reverse()
        atr = atr_wilders(dfdata)
        DIPlus = (smoothed_list[0][0]/atr) * 100
        DIMinus = (smoothed_list[0][1]/atr) * 100
        # DX = (abs(DIPlus - DIMinus)/abs(DIPlus + DIMinus)) * 100
        DILists.append([DIPlus, DIMinus])

    return DILists
